import telebot
from telebot import types
import tiktoks_downloader
from tiktok_analyzer import TikTokAnalyzer
import random
from flask import Flask, request
import os

TOKEN = os.environ["TOKEN_TT"]
server = Flask(__name__)
bot = telebot.TeleBot(TOKEN, threaded=False)
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
            tiktok_info = tiktoks_downloader.get_tiktoks(message.text)
            global tiktok_username
            tiktok_username = message.text
            keyboard2 = types.InlineKeyboardMarkup(row_width=8)
            backbutton2 = types.InlineKeyboardButton(text="Назад в меню", callback_data="mainmenu")
            keyboard2.add(backbutton2)
            q_button = types.InlineKeyboardButton(text="get prediction", callback_data="get prediction")
            w_button = types.InlineKeyboardButton(text="desc", callback_data="desc")
            keyboard2.add(q_button, w_button)

            bot.send_message(message.chat.id,
                             "done",
                             reply_markup=keyboard2)

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


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://horo-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
