import urllib.request, urllib.parse, urllib.error
import pandas as pd
from datetime import datetime
import ast
import json
import requests
import time
from datetime import date,timedelta
from AQIcalculation import calculate_aqi,calculate_aqi_pollutant
# districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']
# api_key = 'a1eb985df9b2ea59efd41ee6a426deee'
# base_url = "http://api.openweathermap.org/data/2.5/weather?"
districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']
def Realtimeweather(district):
    api_key = 'a1eb985df9b2ea59efd41ee6a426deee'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    
    complete_url = base_url + "appid=" + api_key + "&q=" + district
    response = requests.get(complete_url)
    data = response.json()

    # Extract the relevant weather data
    temp_min = round(data['main']['temp_min'] - 273.15, 2)
    temp_max = round(data['main']['temp_max'] - 273.15, 2)
    humidity_min = data['main']['humidity']
    humidity_max = data['main']['humidity']
    wind_speed_min = round(data['wind']['speed'] * 3.6, 2)
    wind_speed_max = round(data['wind']['speed'] * 3.6, 2)
    weather = {'District': district, 'temp_min (⁰C)': temp_min, 'temp_max (⁰C)': temp_max,
                'humidity_min (%)': humidity_min, 'humidity_max (%)': humidity_max, 'wind_speed_min (Kmph)': wind_speed_min,
                'wind_speed_max (Kmph)': wind_speed_max}
    
    
    return weather


def Realtimeaqi(district):
    
    dic = {"Adilabad":"{'lon': 78.5, 'lat': 19.5}", 
            "Nizamabad":"{'lon': 78.25, 'lat': 18.75}",
            "Warangal":"{'lon': 79.5971, 'lat': 17.9821}",
            "Karimnagar":"{'lon': 79.1328, 'lat': 18.4348}",
            "Khammam":"{'lon': 80.3333, 'lat': 17.5}"}
    latlon = ast.literal_eval(dic[district])
    
    lat = latlon['lat']
    lon = latlon['lon']

    # Construct the API URL with the required parameters
    key = "c07a9fcaab2d950fbcc19fef00a77360"
    serviceURL = "http://api.openweathermap.org/data/2.5/air_pollution?"
    url = f"{serviceURL}lat={lat}&lon={lon}&appid={key}"
    
    # Send a request to the API URL and receive the response
    response = urllib.request.urlopen(url)

    # Parse the response JSON data into a dataframe    
    data = json.loads(response.read().decode())
    aqi_data = calculate_aqi(data)
    
    aqi,pollutant_concentrations, = aqi_data
    # print(pollutant_concentrations)
    # print(aqi)
    return aqi,pollutant_concentrations
    
