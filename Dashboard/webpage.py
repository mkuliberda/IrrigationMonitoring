from flask import Flask, render_template
import requests
#from pusher import Pusher

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = False

@app.route('/')
def index():
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
    city = 'Gdansk'

    r = requests.get(weather_url.format(city)).json()
    print(r)

    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'real_feel' : r['main']['feels_like'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(weather)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
