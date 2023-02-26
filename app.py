import json
# from urllib import request
from flask import Flask, jsonify , render_template , url_for , request
from weather_aqi import Realtimeweather,Realtimeaqi

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
    return jsonify({'result':Realtimeaqi(loc)})    

@app.route('/aqi')
def aqi():
    return render_template('aqi.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')
    
if __name__ == '__main__':
    app.run(host='localhost', port=8080)