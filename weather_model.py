import pandas as pd
import numpy as np
import seaborn as sns
from datetime import date,timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

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

def Weatherrunner():

def Weather_dataConsistence():
#     dic = {"Adilabad":"{'lon': 78.5, 'lat': 19.5}", 
#             "Nizamabad":"{'lon': 78.25, 'lat': 18.75}",
#             "Warangal":"{'lon': 79.5971, 'lat': 17.9821}",
#             "Karimnagar":"{'lon': 79.1328, 'lat': 18.4348}",
#             "Khammam":"{'lon': 80.3333, 'lat': 17.5}"}
#     latlon = ast.literal_eval(dic[district])
    
#     lat = latlon['lat']
#     lon = latlon['lon']
