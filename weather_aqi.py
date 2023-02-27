import urllib.request, urllib.parse, urllib.error
import pandas as pd
import datetime
import ast
import json
import requests
import time
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

# def loc_in_latlon(district):
#     dic = {"Adilabad":"{'lon': 78.5, 'lat': 19.5}", 
#             "Nizamabad":"{'lon': 78.25, 'lat': 18.75}",
#             "Warangal":"{'lon': 79.5971, 'lat': 17.9821}",
#             "Karimnagar":"{'lon': 79.1328, 'lat': 18.4348}",
#             "Khammam":"{'lon': 80.3333, 'lat': 17.5}"}
#     latlon = ast.literal_eval(dic[district])
#     return latlon

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
    
while True:
    districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']
    for district in districts:
        data = Realtimeaqi(district)
        aqi,pollutant_concentrations = data
        df = pd.read_csv('Data/AQI Data/AQI_finaldataset.csv')
        pcc = pd.DataFrame.from_dict(pollutant_concentrations, orient='index', columns=['Values'], dtype=None)
        pcc = pcc.transpose()

        # Get today's date
        today = datetime.today().strftime('%Y-%m-%d')

        # Group the existing data by date and district to get the mean AQI values for each day
        df_grouped = df.groupby(['Date', 'Location']).mean().reset_index()

        # Check if there is an existing record for today's date and district
        mask = (df_grouped['Date'] == today) & (df_grouped['Location'] == district+", Telangana, India")

        # If there is an existing record, replace it with the new data
        if mask.any():
            df_grouped.loc[mask, 'AQI'] = aqi ['AQI']
            for key, value in pollutant_concentrations.items():
                df_grouped.loc[mask, key] = value

        # If there is no existing record, add a new row with the new data
        else:
            new_row = {'Date': today, 'Location': district+", Telangana, India", 'AQI': aqi['AQI']}
            for key, value in pollutant_concentrations.items():
                new_row[key] = value
            df_grouped = df_grouped.append(new_row, ignore_index=True)

        # Save the updated data to the CSV file
        df_grouped.to_csv('/home/suku/Desktop/projects/T-aims/nasccom/Data/Air_Quality_Index/AQI_finaldataset copy.csv', index=False)
    time.sleep(3600)