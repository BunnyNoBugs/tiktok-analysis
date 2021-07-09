#!/usr/bin/env python
# coding: utf-8

# In[58]:


import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from html import unescape
from datetime import datetime
from datetime import timedelta
from tqdm.auto import tqdm
from typing import List
from typing import Tuple


# ### Функция поиска ссылок

# In[190]:


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


# In[191]:


links = get_links()


# ### Сначала сделаю функции по поиску конкретных данных, потом все в одну большую

# In[61]:


def get_city(soup: str) -> str:
    city_html = soup.select("span.locality span")
    city = city_html[0].attrs["title"]
    return city


# In[62]:


def get_summary(soup: str) -> str:
    summary_html = soup.find_all("span", attrs={'class': 'tooltip'})
    summaries = []
    for i in range(10):
        summary = summary_html[i].get("data-text")
        summaries.append(summary)
    return summary


# In[63]:


def transform_minus(number: str) -> int:
    if '−' in number: #заменяю знак тире на знак минуса, иначе не получается превратить в int
        number = number.replace('−', '-')
    return int(number)


# In[64]:


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
            max_temps.append('None') #добавляю строку с нан, потому что далее при доставании ср темп с обычным наном 
                                      #работать очень неудобно
        if '<div class="mint">' in line:
            min_temp = re.findall('unit_temperature_c">(.+?)</span>', line)
            min_temp = transform_minus(min_temp[1])
            min_temps.append(min_temp)
        else:
            min_temps.append('None')

        if '<div class="mint">' in line and '<div class="maxt">' not in line:
            min_temp = re.findall('unit_temperature_c">(.+?)</span>', line)
            min_temp = transform_minus(min_temp[1])
            min_temps.append(min_temp) #это на случай, если будет только мин temp
                                           #не знаю, бывает ли так, но я перестрахуюсь   
    return max_temps, min_temps


# In[65]:


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
            min_pressures.append(int(min_pressure[0])) #это на случай, если будет только мин давление
                                           #не знаю, бывает ли так, но я перестрахуюсь
    return max_pressures, min_pressures


# In[66]:


def get_precipitations(soup: str) -> List[int]: ###МОЖНО ПЕРЕДЕЛАТЬ С СУПОМ
    
    precipitation_html = soup.find_all('div', {'class': 'w_prec__value'})
    temp_precipitation = re.findall('">(.+?)</div>', str(precipitation_html), re.DOTALL)
    precipitations = []
    for el in temp_precipitation: #через обычную регулярку с (\d.+) у меня почему-то не искало
        prec = re.findall('\d|,', el)
        if len(prec) > 1:
            prec[-2] = '.'
            prec = ''.join(prec)
            precipitations.append(float(prec))
        else:
            precipitations.append(int(prec[0]))
        
    return precipitations


# In[67]:


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


# In[68]:


def load_forecast(link: str) -> List[dict]:
    url = link
    session = requests.session()
    ua = UserAgent(verify_ssl=False)
    req = session.get(url, headers={'User-Agent': ua.chrome})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    city = get_city(soup)

    summary = get_summary(soup)
       
    temps = get_temps(soup)
    
    pressures = get_press(soup)

    max_wind_speeds = get_max_wind_speed(soup)
            
    precipitations = get_precipitations(soup)
            
          
    d =    {
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
    t=0
    for n in range(10):
        date = datetime.now() + timedelta(days=t)
        date = date.strftime("%Y-%m-%d"),  #НАДО МЕНЯТЬ ДАТУ!
        

        d = {
            'date': date[0],
            'city': city,
            'summary': summary,
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
        t+=1
        
    return l_forecast


# ### Все прогнозы

# In[69]:


def load_all_forecasts() -> List[dict]:
    links = get_links()
    del links[10:]
    
    forecasts = []
    for link in links:
        city_forecast = load_forecast(link)
        for day in city_forecast:
            forecasts.append(day)
    return forecasts


# In[70]:


fr = load_all_forecasts()


# ### Дф

# In[205]:


import pandas as pd


# In[210]:


df = pd.DataFrame(fr)
datetimes = pd.to_datetime(df["date"])
df["date"] = datetimes
df


# In[214]:


i=0
rolls_temps = []
for i in range(10):
    rolling_df = df[i:i+10]
    roll = rolling_df['max_temp'].rolling(3).mean()
    i+=10
    rolls_temps.append(roll)

rolls_for_city = []
for roll in rolls_temps:
    for temp in roll:
        rolls_for_city.append(temp)

df['max_temp_rolling'] = rolls_for_city


# In[215]:


df


# In[75]:


df['day_of_week'] = df['date'].dt.dayofweek


# In[76]:


df


# ### Поиск теплейших выходных

# In[180]:


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


# In[182]:


def find_best_city(df: pd.DataFrame) -> str:
    max_df = get_aver_temp(df)
    highest_temp = {}
    weekends = [] 
    for ind, day in enumerate(max_df['day_of_week']):
        if len(weekends) > 0:
            weekends.append((ind, day))

            if weekends[-2][1] == 5:
                aver_w_temp = (max_df['average_temp'][weekends[ind-1][0]] + max_df['average_temp'][ind]) / 2
                highest_temp[max_df['city'][ind]] = aver_w_temp

        else:
            weekends.append((ind, day))

    highest_temp = dict(sorted(highest_temp.items(), key=lambda item: item[1]))
    return list(highest_temp.keys())[-1]


# In[183]:


find_best_city(df)


# In[ ]:





# In[ ]:




