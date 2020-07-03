
from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import socket
import time

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
    city = 'Gdansk'

    curr = requests.get(weather_url.format(city)).json()
    fore = requests.get(forecast_url.format(city)).json()

    current_weather = {
        'city': city,
        'temperature': curr['main']['temp'],
        'real_feel' : curr['main']['feels_like'],
        'humidity' : curr['main']['humidity'],
        'description': curr['weather'][0]['description'],
        'icon': curr['weather'][0]['icon'],
        'last_update': '10s'
    }

    forecast_3hr = {
        'city': city,
        'time': fore['list'][1]['dt_txt'],
        'real_feel': fore['list'][1]['main']['feels_like'],
        'description': fore['list'][1]['weather'][0]['description'],
        'icon': fore['list'][1]['weather'][0]['icon'],
        'rain': 0,
        'last_update': '15s'
    }
    for i in range(30):
        if fore['list'][i]['weather'][0]['main'] == 'Rain':
            forecast_3hr['time'] = fore['list'][i]['dt_txt']
            forecast_3hr['description'] = fore['list'][i]['weather'][0]['description']
            forecast_3hr['icon'] = fore['list'][i]['weather'][0]['icon']
            forecast_3hr['rain'] = fore['list'][i]['rain']['3h']
            forecast_3hr['real_feel'] = fore['list'][i]['main']['feels_like']
            break

    return render_template('index.html', current_weather=current_weather, forecast_3hr=forecast_3hr)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8082, debug=True)


