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
    data = pd.read_csv("/Users/aman/Desktop/NASSCOM/TheScripter-s/Preprocessing/Weather/all_data.csv")

    df = data[data['Location'] == district]

    df['Date'] = pd.to_datetime(df['Date']).dt.date

    train_end_date, train_start_date, pred_start_date, pred_end_date = datesForForecast()

    temp = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'), 'Location': district,
                         'Minimum Temperature': 0,
                         'Maximum Temperature': 0, 'Relative Humidity': 0})

    df = pd.concat([df, temp])

    df['Date'] = pd.to_datetime(df['Date']).dt.date

    df = df.set_index('Date')

    train_data = df[train_start_date:train_end_date].reset_index(drop=False)

    model_min_temp = SARIMAX(train_data['Minimum Temperature'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_min_temp = model_min_temp.fit()

    model_max_temp = SARIMAX(train_data['Maximum Temperature'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_max_temp = model_max_temp.fit()

    model_humidity = SARIMAX(train_data['Relative Humidity'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results_humidity = model_humidity.fit()

    test_data = df[pred_start_date:pred_end_date].reset_index(drop=False)

    start_date = test_data.index[0]
    end_date = test_data.index[-1]

    temp_min_predictions = results_min_temp.predict(start=start_date, end=end_date, dynamic=False)

    temp_max_predictions = results_max_temp.predict(start=start_date, end=end_date, dynamic=False)

    humidity_predictions = results_humidity.predict(start=start_date, end=end_date, dynamic=False)

    predictions = pd.DataFrame(
        {'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'), 'Location': district,
         'Minimum Temperature': temp_min_predictions,
         'Maximum Temperature': temp_max_predictions, 'Relative Humidity': humidity_predictions})

    return predictions


districts = ['Adilabad', 'Nizamabad', 'Khammam', 'Karimnagar', 'Warangal']


def weather_runner():
    all_predictions = pd.DataFrame(
        columns=['Date', 'Location', 'Minimum Temperature', 'Maximum Temperature', 'Relative Humidity' ])
    for district in districts:
        predictions = weather_forecast(district)
        predictions = predictions.drop_duplicates()
        all_predictions = pd.concat([all_predictions, predictions], axis=0, ignore_index=True)

    all_predictions = all_predictions[all_predictions['Date'] != str(date.today())]
    all_predictions.to_csv("weather_forecast.csv", index=False)



# def dataConsistence():
#     dic = {"Adilabad":"{'lon': 78.5, 'lat': 19.5}", 
#             "Nizamabad":"{'lon': 78.25, 'lat': 18.75}",
#             "Warangal":"{'lon': 79.5971, 'lat': 17.9821}",
#             "Karimnagar":"{'lon': 79.1328, 'lat': 18.4348}",
#             "Khammam":"{'lon': 80.3333, 'lat': 17.5}"}
#     latlon = ast.literal_eval(dic[district])
    
#     lat = latlon['lat']
#     lon = latlon['lon']
