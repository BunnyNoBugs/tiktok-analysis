import telebot
from telebot import types
import conf
import tiktok_api
from tiktok_analyzer import TikTokAnalyzer
import random

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
tiktok_info = True
tiktok_username = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=8)
    first_button = types.InlineKeyboardButton(text="start", callback_data="start")
    second_button = types.InlineKeyboardButton(text="help", callback_data="help")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который покажет вам статистику выбранного тикток профиля",
                     reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=8)
        first_button = types.InlineKeyboardButton(text="start", callback_data="start")
        second_button = types.InlineKeyboardButton(text="help", callback_data="help")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Вы вернулись в меню",
                              reply_markup=keyboardmain)
        pass

    elif call.data == "help":
        keyboard = types.InlineKeyboardMarkup(row_width=8)
        backbutton = types.InlineKeyboardButton(text="Назад в меню", callback_data="mainmenu")
        keyboard.add(backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text='Это бот, который может выдать некоторую \
                                                                       статистику по пользователю тиктока'
                              , reply_markup=keyboard)
        pass

    elif call.data == "start":
        keyboard = types.InlineKeyboardMarkup(row_width=8)
        backbutton = types.InlineKeyboardButton(text="Назад в меню", callback_data="mainmenu")
        keyboard.add(backbutton)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Введите никнейм и выберите интересующую информацию. \
                                    Введите любой никнейм повторно, чтобы узнать про другого пользователя.',
                              reply_markup=keyboard)

        @bot.message_handler(content_types=['text'])
        def send_text(message):
            global tiktok_info
            bot.send_message(message.chat.id, 'getting')
            tiktok_info = tiktok_api.get_tiktoks(message.text)
            global tiktok_username
            tiktok_username = message.text
            # tiktok_info = 'asdasdasda'
            keyboard2 = types.InlineKeyboardMarkup(row_width=8)
            backbutton2 = types.InlineKeyboardButton(text="Назад в меню", callback_data="mainmenu")
            keyboard2.add(backbutton2)
            q_button = types.InlineKeyboardButton(text="get prediction", callback_data="get prediction")
            w_button = types.InlineKeyboardButton(text="desc", callback_data="desc")
            keyboard2.add(q_button, w_button)

            bot.send_message(message.chat.id,
                             "done",
                             reply_markup=keyboard2)
            # return tiktok_info
            # @bot.callback_query_handler(func=lambda call1: True)
            # def callback_inline1(call1):
            #    print('111')
            #    print(call.data)

        pass

    elif call.data == "get prediction":
        if len(tiktok_info) < 50:
            bot.send_message(chat_id=call.message.chat.id,
                             text="У данного юзера слишком мало тиктоков для предсказания")
        else:
            analyser = TikTokAnalyzer(tiktok_info, username=tiktok_username)
            pred = analyser.predict_likes()
            path_to_plot = 'tmp/prediction.png'
            analyser.plot_likes_prediction(pred, path=path_to_plot)
            with open(path_to_plot, 'rb') as f:
                plot = f.read()
            bot.send_photo(chat_id=call.message.chat.id, photo=plot)
            pass
        pass

    elif call.data == "desc":
        try:
            random_tiktok = random.choice(tiktok_info)
            bot.send_message(chat_id=call.message.chat.id,
                             text=f"{random_tiktok['desc']}\nКоличество лайков: {random_tiktok['stats']['diggCount']}")
            pass
        except IndexError:
            bot.send_message(chat_id=call.message.chat.id, text="Нет описания")
        pass


if __name__ == '__main__':
    bot.polling()
