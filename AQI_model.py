# Importing Required Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import ast
import json
import urllib.request, urllib.parse, urllib.error
from datetime import datetime,timedelta
from datetime import date,timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from weather_aqi import Realtimeaqi

def datesForForecast():
    train_end_date = date.today() - timedelta(days=2)
    train_start_date = train_end_date - timedelta(days=672)
    pred_start_date = date.today() + timedelta(days=1)
    pred_end_date = pred_start_date + timedelta(days=183)
    
    return train_end_date,train_start_date,pred_start_date,pred_end_date

def AQI_forecast(district):
    data = pd.read_csv("/home/suku/Desktop/projects/T-aims/TheScripter-s/Preprocessing/AQI/AQI.csv")
    df = data[data['Location']==district]
   
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    
    temp = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'),'Location': district,'AQI':0,'NO2':0,'SO2':0, 'PM2.5':0, 'PM10':0})
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
    
    no2_predictions = results_no2.predict(start=start_date, end=end_date, dynamic=False)
    
    so2_predictions = results_so2.predict(start=start_date, end=end_date, dynamic=False)
    
    pm25_predictions = results_pm25.predict(start=start_date, end=end_date, dynamic=False)
    
    pm10_predictions = results_pm10.predict(start=start_date, end=end_date, dynamic=False)

    predictions = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'),'Location': district,'AQI': aqi_predictions, 
                                'NO2':no2_predictions,'SO2':so2_predictions,'PM2.5':pm25_predictions,'PM10':pm10_predictions})
    
    return predictions
    
    


def AQIrunner():
    all_predictions = pd.DataFrame(columns=['Date', 'Location', 'AQI', 'NO2', 'SO2', 'PM2.5', 'PM10'])
    for district in districts:
        predictions = AQI_forecast(district)
        predictions = predictions.drop_duplicates()
        all_predictions = pd.concat([all_predictions, predictions], axis=0, ignore_index=True)
        
        
    all_predictions.to_csv("/home/suku/Desktop/projects/T-aims/TheScripter-s/Preprocessing/AQI/AQI_forecast.csv", index=False)



def AQI_dataConsistence():
    # Read existing data from AQI.csv file
    
    data = pd.read_csv("AQI.csv")

    # Define dictionary of district names and their corresponding lat/lon coordinates
    districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']
    # Loop over each district and get AQI and pollutant concentration data
    for district in districts:
        aqi, all_pollutants = Realtimeaqi(district)
        
        # Create dictionary of data to append to AQI.csv
        data_to_append = {"Date": datetime.today().strftime('%Y-%m-%d'),
                        "Location": district,
                        "AQI": aqi['AQI'],
                        # "CO": all_pollutants.get('CO', ''),
                        # "NO": all_pollutants.get('NO', ''),
                        "NO2": all_pollutants.get('NO2', ''),
                        # "O3": all_pollutants.get('O3', ''),
                        "SO2": all_pollutants.get('SO2', ''),
                        "PM2.5": all_pollutants.get('PM2.5', ''),
                        "PM10": all_pollutants.get('PM10', '')
                        # "NH3": all_pollutants.get('NH3', ''),
                        # "Latitude": lat,
                        # "Longitude": lon
                        }
        
        # Append data to AQI.csv file
        data = data.append(data_to_append, ignore_index=True)

    # Write updated data to AQI.csv file
    data  = data.groupby(['Date', 'Location']).mean()
    data.to_csv("AQI.csv", index=False)

    
