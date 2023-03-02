import pandas as pd
import numpy as np
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf



def fit_and_forecast(variable, train_data, test_data):
    # Creating SARIMAX Model
    model = SARIMAX(train_data[variable], order=(1, 1, 0), seasonal_order=(1, 0, 1, 12))
    results = model.fit()

    # Predicting Variable
    start_date = test_data.index[0]
    end_date = test_data.index[-1]
    predictions = results.predict(start=start_date, end=end_date, dynamic=False)
        
    return predictions

def runner():
    districts = ['Adilabad', 'Nizamabad',  'Khammam', 'Karimnagar',  'Warangal']
    for district in districts :
        df = pd.read_csv('weather_data.csv', index_col='Date', parse_dates=True)
        
        df_adilabad = df[df['District'] == district]
        
        
        
        temp_min_predictions = fit_and_forecast('temp_min (⁰C)', train_data, test_data)
        temp_max_predictions = fit_and_forecast('temp_max (⁰C)', train_data, test_data)
        humidity_min_predictions = fit_and_forecast('humidity_min (%)', train_data, test_data)
        humidity_max_predictions = fit_and_forecast('humidity_max (%)', train_data, test_data)
        wind_speed_min_predictions = fit_and_forecast('wind_speed_min (Kmph)', train_data, test_data)
        wind_speed_max_predictions = fit_and_forecast('wind_speed_max (Kmph)', train_data, test_data)


        