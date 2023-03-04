import json
import pandas as pd
# from urllib import request
from flask import Flask, jsonify , render_template , url_for , request
from weather_aqi import Realtimeweather,Realtimeaqi
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from AQI_model import AQIrunner , AQI_dataConsistence
from weather_model import  weather_runner,Weather_dataConsistence
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')
    
@app.route('/api/weather',methods=['POST'])
def Realweather():

    loc = json.loads(request.data).get('loc')
    print(loc)
    return jsonify({'result':Realtimeweather(loc)})
    
@app.route('/api/aqi',methods=['POST'])
def Realaqi():

    loc = json.loads(request.data).get('loc')
    print(loc)
    aqi_data, pollutant_data = Realtimeaqi(loc)
    result = {'AQI': aqi_data['AQI'],"Main Pollutant": aqi_data['Main pollutant'],"value":aqi_data['value']}
    for pollutant, conc in pollutant_data.items():
        result[pollutant] = conc
    return jsonify({'result': result})   


@app.route('/aqi')
def aqi():
    return render_template('aqi.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

    
@app.route('/plot/weather', methods=['GET', 'POST'])
def weatherPlot():
    loc = request.args.get('loc')
    weatherVar = request.args.get('weatherVar')

    # Load weather forecast data for the specified location
    df = pd.read_csv('Data/Weather_Data/weather_forecast.csv')
    df = df[df['Location'] == loc]
    # Extract x and y data based on selected weather variable
    if weatherVar == "MinTemp":
        x = df['Date']
        y = df['Minimum Temperature']
    elif weatherVar == "MaxTemp":
        x = df['Date']
        y = df['Maximum Temperature']
    elif weatherVar == "Humidity":
        x = df['Date']
        y = df['Relative Humidity']
    elif weatherVar == "HeatWaveIndex":
    # Calculate heat wave index and add to dataframe
        hw_index = []
        max_temp = df['Maximum Temperature']
        temp_threshold = 40
        for i in range(len(max_temp)):
            if max_temp[i] >= temp_threshold:
                if i > 0 and hw_index[i-1] > 0:
                    hw_index.append(hw_index[i-1] + 1)
                else:
                    hw_index.append(1)
            else:
                hw_index.append(0)
        df['HeatWaveIndex'] = hw_index
        x = df['Date']
        y = df['HeatWaveIndex']

    return jsonify({'x': x.tolist(), 'y': y.tolist(), 'loc': loc, 'weatherVar': weatherVar})





@app.route('/plot/aqi', methods=['GET', 'POST'])
def AqiPlot():
    loc = request.args.get('loc')
    aqiVar = request.args.get('aqiVar')
    df = pd.read_csv('Data/AQI_Data/AQI_forecast.csv')
    df = df[df['Location'] == loc ]
    if aqiVar == 'AQI' :
        x = df['Date']
        y = df['AQI']
    elif aqiVar == 'PM2.5' :
        x = df['Date']
        y = df['PM2.5']
    elif aqiVar == 'PM10' :
        x = df['Date']
        y = df['PM10']
    elif aqiVar == 'NO2' :
        x = df['Date']
        y = df['NO2']
    elif aqiVar == 'SO2' :
        x = df['Date']
        y = df['SO2']
    return jsonify({'x': x.tolist(), 'y': y.tolist(), 'loc': loc ,'aqiVar': aqiVar})

def Model_Trainer():
    AQIrunner()
    weather_runner()

def dataConsistence():
    AQI_dataConsistence()
    Weather_dataConsistence()
    
if __name__ == '__main__':
    app.run(host='localhost', port=8080 ,debug=True)
    scheduler = BackgroundScheduler()
    scheduler.add_job(Model_Trainer, 'interval', days=7, start_date=datetime.today())
    scheduler.add_job(dataConsistence, 'interval', hours=2, start_date=datetime.today())
    scheduler.start()