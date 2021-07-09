import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Tuple
import json
import pandas as pd


# Антон Арцишевский

# функция поиска ссылок
def get_links() -> list:
    url = 'https://www.gismeteo.ru/'
    session = requests.session()
    ua = UserAgent(verify_ssl=False)
    req = session.get(url, headers={'User-Agent': ua.chrome})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    links_block = soup.find_all(id="noscript")

    for temp_link in links_block:
        temp_links = re.findall('href="(.+?)"', str(temp_link))

    links = []
    for link in temp_links:
        new_link = 'https://www.gismeteo.ru' + link + '10-days/'
        links.append(new_link)

    return links


# сначала сделаю функции по поиску конкретных данных, потом все в одну большую
def get_city(soup: str) -> str:
    city_html = soup.select("span.locality span")
    city = city_html[0].attrs["title"]
    return city


def get_summary(soup: str) -> str:
    summary_html = soup.find_all("span", attrs={'class': 'tooltip'})
    summaries = []
    for i in range(10):
        summary = summary_html[i].get("data-text")
        summaries.append(summary)
    return summaries


def transform_minus(number: str) -> int:
    if '−' in number:  # заменяю знак тире на знак минуса, иначе не получается превратить в int
        number = number.replace('−', '-')
    return int(number)


def get_temps(soup: str) -> Tuple[list]:
    data_html = soup.find_all(attrs={'class': 'values'})
    temp_html = data_html[0]
    max_temps = []
    min_temps = []

    for line in temp_html:
        line = str(line)
        if '<div class="maxt">' in line:
            max_temp = re.findall('unit_temperature_c">(.+?)</span>', line)
            max_temp = transform_minus(max_temp[0])
            max_temps.append(max_temp)
        else:
            max_temps.append('None')  # добавляю строку с нан, потому что далее при доставании ср темп с обычным наном
            # работать очень неудобно
        if '<div class="mint">' in line:
            min_temp = re.findall('unit_temperature_c">(.+?)</span>', line)
            min_temp = transform_minus(min_temp[1])
            min_temps.append(min_temp)
        else:
            min_temps.append('None')

        if '<div class="mint">' in line and '<div class="maxt">' not in line:
            min_temp = re.findall('unit_temperature_c">(.+?)</span>', line)
            min_temp = transform_minus(min_temp[1])
            min_temps.append(min_temp)  # это на случай, если будет только мин temp
            # не знаю, бывает ли так, но я перестрахуюсь
    return max_temps, min_temps


def get_press(soup: str) -> Tuple[list]:
    data_html = soup.find_all(attrs={'class': 'values'})
    pres_html = data_html[-1]
    max_pressures = []
    min_pressures = []

    for line in pres_html:
        line = str(line)
        if '<div class="maxt">' in line:
            max_pressure = re.findall('unit_pressure_mm_hg_atm">(.+?)</span>', line)
            max_pressures.append(int(max_pressure[0]))
        else:
            max_pressures.append('None')

        if '<div class="mint">' in line:
            min_pressure = re.findall('unit_pressure_mm_hg_atm">(.+?)</span>', line)
            min_pressures.append(int(min_pressure[1]))
        else:
            min_pressures.append('None')

        if '<div class="mint">' in line and '<div class="maxt">' not in line:
            min_pressure = re.findall('unit_pressure_mm_hg_atm">(.+?)</span>', line)
            min_pressures.append(int(min_pressure[0]))  # это на случай, если будет только мин давление
            # не знаю, бывает ли так, но я перестрахуюсь
    return max_pressures, min_pressures


def get_precipitations(soup: str) -> List[int]:
    precipitation_html = soup.find_all('div', {'class': 'w_prec__value'})
    temp_precipitation = re.findall('">(.+?)</div>', str(precipitation_html), re.DOTALL)
    precipitations = []
    for el in temp_precipitation:  # через обычную регулярку с (\d.+) у меня почему-то не искало
        prec = re.findall('\d|,', el)
        if len(prec) > 1:
            prec[-2] = '.'
            prec = ''.join(prec)
            precipitations.append(float(prec))
        else:
            precipitations.append(int(prec[0]))

    return precipitations


def get_max_wind_speed(soup: str) -> List[int]:
    max_wind_speeds = []
    max_wind_speed_html = soup.select("span.unit_wind_m_s")
    for line in max_wind_speed_html:
        line = str(line)
        if 'unit unit_wind_m_s' in line:
            speed = re.findall('\d+', line)
            max_wind_speeds.append(int(speed[0]))
            if len(max_wind_speeds) == 10:
                break

    return max_wind_speeds


def load_forecast(link: str) -> List[dict]:
    url = link
    session = requests.session()
    ua = UserAgent(verify_ssl=False)
    req = session.get(url, headers={'User-Agent': ua.chrome})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    city = get_city(soup)

    summaries = get_summary(soup)

    temps = get_temps(soup)

    pressures = get_press(soup)

    max_wind_speeds = get_max_wind_speed(soup)

    precipitations = get_precipitations(soup)

    d = {
        'date': str,
        'city': str,
        'summary': str,
        'max_temp': int or str,
        'min_temp': int or str,
        'max_wind_speed': int,
        'precipitation': int,
        'min_pressure': int or str,
        'max_pressure': int or str,
    }

    l_forecast = []
    t = 0
    for n in range(10):
        date = datetime.now() + timedelta(days=t)
        date = date.strftime("%Y-%m-%d"),  # НАДО МЕНЯТЬ ДАТУ!

        d = {
            'date': date[0],
            'city': city,
            'summary': summaries[n],
            'max_temp': temps[0][n],
            'min_temp': temps[1][n],
            'max_wind_speed': max_wind_speeds[n],
            'precipitation': precipitations[n],
            'max_pressure': pressures[0][n],
            'min_pressure': pressures[1][n],
        }
        l_forecast.append(d)

        date = datetime.now()
        date += timedelta(days=1)
        t += 1

    return l_forecast


# все прогнозы
def load_all_forecasts() -> List[dict]:
    links = get_links()
    del links[10:]

    forecasts = []
    for link in links:
        city_forecast = load_forecast(link)
        for day in city_forecast:
            forecasts.append(day)
    return forecasts


# функция преобразавания даты и дней недели в дф (в задании не сказано сделать функцией
# но это как-то странно и неудобно (могу сделать и так, не снижайте))
def transform_date_week(df: pd.DataFrame) -> pd.DataFrame:
    datetimes = pd.to_datetime(df["date"])
    df["date"] = datetimes
    df['day_of_week'] = df['date'].dt.dayofweek
    return df


def get_rolls(df: pd.DataFrame) -> pd.DataFrame:
    i = 0
    rolls_temps = []
    for i in range(10):
        rolling_df = df[i:i + 10]
        roll = rolling_df['max_temp'].rolling(3).mean()
        i += 10
        rolls_temps.append(roll)

    rolls_for_city = []
    for roll in rolls_temps:
        for temp in roll:
            rolls_for_city.append(temp)

    df['max_temp_rolling'] = rolls_for_city
    return df


# поиск теплейших выходных
def get_aver_temp(df: pd.DataFrame) -> pd.DataFrame:
    max_df = df
    average_temps = []
    for index, row in max_df.iterrows():
        if row['min_temp'] == 'None':
            average_temps.append((row['max_temp'] + row['max_temp']) / 2)

        else:
            average_temps.append((row['max_temp'] + row['min_temp']) / 2)

    max_df['average_temp'] = [i for i in average_temps]

    return max_df


def find_best_city(df: pd.DataFrame) -> str:
    max_df = get_aver_temp(df)
    highest_temp = {}
    weekends = []
    for ind, day in enumerate(max_df['day_of_week']):
        if len(weekends) > 0:  # обход того, что вначале список пустой
            weekends.append((ind, day))

            if weekends[-2][1] == 5:  # я сначала добавляю день, поэтому для позапрошлого надо брать -2
                aver_w_temp = (max_df['average_temp'][weekends[ind - 1][0]] + max_df['average_temp'][ind]) / 2
                highest_temp[max_df['city'][ind]] = aver_w_temp

        else:
            weekends.append((ind, day))

    highest_temp = dict(sorted(highest_temp.items(), key=lambda item: item[1]))
    return list(highest_temp.keys())[-1]


def get_iata(IATA: str) -> str:
    url = 'https://www.travelpayouts.com/widgets_suggest_params?q=Из%20Москвы%20в%20' + IATA
    session = requests.session()
    req = session.get(url, stream=True)
    html = req.text
    iata = json.loads(html)
    iata = iata['destination']['iata']
    return iata


def get_saturday() -> str:
    date = datetime.now()
    while date.weekday() != 5:
        date += timedelta(days=1)
    date = date.strftime("%Y-%m-%d")
    return date


def find_cheapest_ticket(city: str) -> dict:
    iata = get_iata(city)
    date = get_saturday()
    params = {
        'origin': 'MOW',
        'destination': iata,
        'depart_date': date,  # он не учитывает дату при отправлении, бака
        'one_way': 'true'
    }
    av_response = requests.get('http://min-prices.aviasales.ru/calendar_preload', params=params)

    tickets = av_response.text
    tickets = json.loads(tickets)

    bests = []
    for i in tickets['best_prices']:
        if i['depart_date'] == '2020-12-19':
            bests.append(i['value'])
    bests_sorted = sorted(bests)
    best = {'price': bests_sorted[-1]}

    if len(bests) == 0:
        bests.append('No tickets, sorry')
        best = {'error_text': bests}

    return best


def kuda():
    links = get_links()
    forecasts = load_all_forecasts()

    df = pd.DataFrame(fr)
    df = transform_date_week(df)
    df = get_rolls(df)

    best_city = find_best_city(df)
    ticket = find_cheapest_ticket(best_city)

    if len(ticket) != 0:
        print('Можно свалить в город ' + best_city + " за " + str(ticket['price']) + ' рубасов')
    else:
        print('Лучше всего свалить в город ' + best_city + ', но билетов нет')


if __name__ == '__main__':  # непонятно, надо ли мейн, но вот он)
    links = get_links()  # последняя функция по-факту копирует его
    print(len(links))
    fr = load_all_forecasts()
    print(len(fr))
    #df = pd.DataFrame(fr)
    #df = transform_date_week(df)
    #df = get_rolls(df)

    #best_city = find_best_city(df)
    # print(best_city)

    #ticket = find_cheapest_ticket(best_city)
    # print(ticket['price'])

    #kuda_vail = kuda()
    #kuda_vail
