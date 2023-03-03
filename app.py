import json
import pandas as pd
# from urllib import request
from flask import Flask, jsonify , render_template , url_for , request
from weather_aqi import Realtimeweather,Realtimeaqi
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from AQI_model import AQIrunner , AQI_dataConsistence
from weather_model import  Weather_dataConsistence
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
def WeatherPlot():
    loc = request.args.get('loc')
    df = pd.read_csv('Preprocessing/Weather/all_data.csv')
    df = df[df['Location'] == loc]
    x = df['Date']
    y = df['Minimum Temperature']
    return jsonify({'x': x.tolist(), 'y': y.tolist(), 'loc': loc})


@app.route('/plot/aqi', methods=['GET', 'POST'])
def AqiPlot():
    loc = request.args.get('loc')
    df = pd.read_csv('Preprocessing/AQI/AQI.csv')
    df = df[df['Location'] == loc ]
    x = df['Date']
    y = df['AQI']
    return jsonify({'x': x.tolist(), 'y': y.tolist(), 'loc': loc })

def Model_Trainer():
    AQIrunner()
    # Weatherrunner()

def dataConsistence():
    AQI_dataConsistence()
    Weather_dataConsistence()
    
if __name__ == '__main__':
    app.run(host='localhost', port=8080)
    scheduler = BackgroundScheduler()
    scheduler.add_job(Model_Trainer, 'interval', days=7, start_date=datetime.today())
    scheduler.add_job(dataConsistence, 'interval', hours=2, start_date=datetime.today())
    scheduler.start()