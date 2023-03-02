



data = pd.read_csv("AQI_data.csv")


def forecast(data, district, train_start_date, train_end_date, pred_start_date, pred_end_date):
    
    df = data[data['Location']==district]
    
    temp = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'),'Location': district,'AQI':0,'NO2':0,'SO2':0, 'PM2.5':0, 'PM10':0})
    
    df = pd.concat([df, temp])

    df['Date'] = pd.to_datetime(df['Date']).dt.date

    df = df.set_index('Date')

    train_data = df[train_start_date:train_end_date].reset_index(drop=False)

    test_data = df[pred_start_date:pred_end_date].reset_index(drop=False)
    
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



    start_date = test_data.index[0]
    end_date = test_data.index[-1]



    aqi_predictions = results_aqi.predict(start=start_date, end=end_date, dynamic=False)
    
    no2_predictions = results_no2.predict(start=start_date, end=end_date, dynamic=False)
    
    so2_predictions = results_so2.predict(start=start_date, end=end_date, dynamic=False)
    
    pm25_predictions = results_pm25.predict(start=start_date, end=end_date, dynamic=False)
    
    pm10_predictions = results_pm10.predict(start=start_date, end=end_date, dynamic=False)

    predictions = pd.DataFrame({'Date': pd.date_range(pred_start_date, pred_end_date, freq='D'),'Location': location,'AQI': aqi_predictions, 
                                'NO2':no2_predictions,'SO2':so2_predictions,'PM2.5':pm25_predictions,'PM10':pm10_predictions})
    
    return predictions
    
    
    
