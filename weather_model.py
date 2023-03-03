import pandas as pd
import numpy as np
import seaborn as sns
import io
from datetime import date,timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import requests
import datetime

def datesForForecast():
    train_end_date = date.today() - timedelta(days=1)
    train_start_date = train_end_date - timedelta(days=672)
    pred_start_date = date.today() + timedelta(days=1)
    pred_end_date = pred_start_date + timedelta(days=183)
    
    return train_end_date,train_start_date,pred_start_date,pred_end_date

def weather_forecast(district):
    data = pd.read_csv("/home/suku/Desktop/projects/T-aims/TheScripter-s/Preprocessing/Weather/all_data.csv")
    df = data[data['Location']==district]
   
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    
    temp = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'),'Location': district,'Minimum Temperature':0,'Maximum Temperature':0,'SO2':0, 'PM2.5':0, 'PM10':0})
    df = pd.concat([df, temp])
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.set_index('Date')
    
    train_end_date, train_start_date, pred_start_date, pred_end_date = datesForForecast()

    train_data = df[train_start_date:train_end_date].reset_index(drop=False)
    test_data = df[pred_start_date:pred_end_date].reset_index(drop=False)
    
    start_date = test_data.index[0]
    end_date = test_data.index[-1]
    # Creating SARIMAX Model
    
    model_aqi = SARIMAX(train_data['AQI'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_aqi = model_aqi.fit()
    
    model_no2 = SARIMAX(train_data['NO2'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_no2 = model_no2.fit()
    
    model_so2 = SARIMAX(train_data['SO2'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_so2 = model_so2.fit()
    
    model_pm25 = SARIMAX(train_data['PM2.5'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_pm25 = model_pm25.fit()
    
    model_pm10 = SARIMAX(train_data['PM10'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_pm10 = model_pm10.fit()


    aqi_predictions = results_aqi.predict(start=start_date, end=end_date, dynamic=False)

# def Weatherrunner():
districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']

def Weather_dataConsistence():
    all_data = pd.read_csv("/home/suku/Desktop/projects/T-aims/TheScripter-s/Preprocessing/Weather/all_data.csv")
    for district in districts:
        url = "https://visual-crossing-weather.p.rapidapi.com/history"

        querystring = {
            "startDateTime": f"{datetime.date.today()}T00:00:00",
            "aggregateHours": "24",
            "location": district,
            "endDateTime": f"{datetime.date.today()}T17:00:00",
            "unitGroup": "us",
            "dayStartTime": "8:00:00",
            "contentType": "csv",
            "dayEndTime": "17:00:00",
            "shortColumnNames": "0"
        }

        headers = {
            "X-RapidAPI-Key": "7441cbd4e1msh52d67d24dda95c5p1f3c23jsn30d64696ccd0",
            "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        response_str = response.text
        df = pd.read_csv(io.StringIO(response_str))
        col = ['Location', 'Date', 'Minimum Temperature', 'Maximum Temperature', 'Temperature', 'Dew Point', 'Relative Humidity', 'Heat Index', 'Wind Speed', 'Wind Gust', 'Wind Direction', 'Wind Chill', 'Precipitation', 'Precipitation Cover', 'Snow Depth', 'Visibility', 'Cloud Cover', 'Sea Level Pressure', 'Weather Type', 'Latitude', 'Longitude', 'Resolved Address', 'Name', 'Info', 'Conditions']
        # col = ['Address,Date time,Minimum Temperature,Maximum Temperature,Temperature,Dew Point,Relative Humidity,Heat Index,Wind Speed,Wind Gust,Wind Direction,Wind Chill,Precipitation,Precipitation Cover,Snow Depth,Visibility,Cloud Cover,Sea Level Pressure,Weather Type,Latitude,Longitude,Resolved Address,Name,Info,Conditions']
        df.columns = col
        df["Date"] = pd.to_datetime(df["Date"])
        df['Minimum Temperature'] = ((df['Minimum Temperature'] - 32)*(5/9))
        # data['Minimum Temperature'] = (data['Minimum Temperature']*(5/9))
        
        df['Maximum Temperature'] = ((df['Maximum Temperature'] - 32)*(5/9))
        # data['Maximum Temperature'] = (data['Maximum Temperature']*(5/9))

        df['Temperature'] = ((df['Temperature'] - 32) * (5/9))
        
        
        all_data = all_data.append(df, ignore_index=True)
        
    all_data  = all_data.groupby(['Date', 'Location']).mean().reset_index(drop=False)    
    all_data.to_csv("df.csv",index=False)
    