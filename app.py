import json
import pandas as pd
# from urllib import request
from flask import Flask, jsonify , render_template , url_for , request
from weather_aqi import Realtimeweather,Realtimeaqi
import weather_aqi
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

@app.route("/plot")
def plot():
    loc = request.args.get("loc")
    data = pd.read_csv("/Users/aman/Desktop/NASSCOM/WeatherData/df_2023_forecasted.csv")
    filtered_data = data[data["District"] == loc]
    x = filtered_data["Date"].tolist()
    y = filtered_data['temp_max (⁰C)'].tolist()
    return render_template("plot.html", x=x, y=y, loc=loc)

    
if __name__ == '__main__':
    app.run(host='localhost', port=8080)
    #weather_aqi.run()