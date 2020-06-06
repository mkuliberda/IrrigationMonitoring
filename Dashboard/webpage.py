from flask import Flask, render_template
import requests
#from pusher import Pusher

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = False

@app.route('/')
def index():
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=63f4d3e36c7caad4496f47edcea1bd23'
    city = 'Gdansk'

    curr = requests.get(weather_url.format(city)).json()
    fore = requests.get(forecast_url.format(city)).json()
    print(fore)

    current_weather = {
        'city': city,
        'temperature': curr['main']['temp'],
        'real_feel' : curr['main']['feels_like'],
        'humidity' : curr['main']['humidity'],
        'description': curr['weather'][0]['description'],
        'icon': curr['weather'][0]['icon']
    }

    forecast_3hr = {

    }
    #print(current_weather)
    return render_template('index.html', current_weather=current_weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
