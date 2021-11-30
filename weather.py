# Extract weather apis

# api call
    # api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime

def get_weather(city):
    weather_key = '179c27185d9e702b92c403f04ab223c3'
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'APPID':weather_key,  'q':city, 'units':'imperial'}
    response = requests.get(url, params=params)

    weather = response.json()
    return weather


def get_tide(lon, lat):
    url = "https://tides.p.rapidapi.com/tides"

    params = {"latitude": '', "longitude": ''}
    params['latitude'] = lat
    params['longitude'] = lon

    headers = {
        'x-rapidapi-host': "tides.p.rapidapi.com",
        'x-rapidapi-key': "36476bd2a1msh97d8675ec2ef9e9p1b04e1jsn55dc18bff266"
    }

    response = requests.request("GET", url, headers=headers, params=params)

    tide = response.json()

    state1 = tide['extremes'][0]['state']
    time1 = tide['extremes'][0]['timestamp']
    time1 = str(datetime.fromtimestamp(time1))
    time1_split = time1.split()

    state2 = tide['extremes'][1]['state']
    time2 = tide['extremes'][1]['timestamp']
    time2 = str(datetime.fromtimestamp(time2))
    time2_split = time2.split()

    print(time1, time2)
    tides = {}
    tides[state1] = time1_split[1]
    tides[state2] = time2_split[1]

    state = []
    time = []
    for k, v in tides.items():
        state.append(k)
        time.append(v)

    tides_str = state[0] + ': ' + time[0] + ' / ' + state[1] + ': ' + time[1]
    return tides_str

