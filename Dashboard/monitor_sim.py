import socket
import json
import time
from websocket_server import WebsocketServer
import threading
import logging
from datetime import datetime
import sys


logging.basicConfig(filename='irrigation.log', filemode='w', format='%(asctime)s-%(levelname)s-%(process)d-%(message)s', level=logging.INFO)

'''try:
  c = 5 / 0
except Exception as e:
    logging.error(e, exc_info=True)'''


sectors_dashboard = [{
    'type': 'sector',
    'last_update': '10s',
    'watering': True,
    'plants': 'ch1, ch2, ch3',
    'errors': 'All good'
    },
    {
    'type': 'sector',
    'last_update': None,
    'watering': False,
    'plants': '',
    'errors':''
    },
    {
    'type': 'sector',
    'last_update': None,
    'watering': False,
    'plants': '',
    'errors':''
    },
    {
    'type': 'sector',
    'last_update': None,
    'watering': False,
    'plants': '',
    'errors':''
    }]

watertanks_dashboard = [{
    'type': 'tank',
    'last_update': '10min',
    'level': 50,
    'errors':''
    }]

batteries_dashboard = [{
    'type': 'power',
    'last_update': '14s',
    'level': 91,
    'state': 'charging',
    'errors': 'overvoltage'
    }]

plants_dashboard = [{
    'type':'plant',
    'last_update': '11s',
    'name': 'Ogorki',
    'soil_moisture': 11
    },
    {
    'type':'plant',
    'last_update': '12s',
    'name': 'Roszponka',
    'soil_moisture': 12
    },
    {
    'type':'plant',
    'last_update': '13s',
    'name': 'Rzodkiewka',
    'soil_moisture': 13
    },
    {
    'type':'plant',
    'last_update': '14s',
    'name': 'Mieta',
    'soil_moisture': 14
    },
    {
    'type':'plant',
    'last_update': '15s',
    'name': 'Szczypior',
    'soil_moisture': 15
    },
    {
    'type':'plant',
    'last_update': '16s',
    'name': 'Salata',
    'soil_moisture': 16
    },
    {
    'type':'plant',
    'last_update': '17s',
    'name': 'Koperek',
    'soil_moisture': 17
    },
    {
    'type':'plant',
    'last_update': '18s',
    'name': 'Pomidor',
    'soil_moisture': 18
    },
    {
    'type':'plant',
    'last_update': '19s',
    'name': 'Papryka',
    'soil_moisture': 19
    }]

weather_dashboard = {
    'city': 'undefined',
    'temperature': -273.15,
    'real_feel' : -273.15,
    'humidity' : 0,
    'description': 'unknown',
    'icon': '',
    'last_update': '1s'
    }

next_rain_dashboard = {
    'city': 'undefined',
    'time': '1990-01-01 00:00:00',
    'real_feel': -273.15,
    'description': 'unknown',
    'icon': '',
    'rain': 0,
    'last_update': '2s'
    }

notification_archive = []
notification = []
i = 0

def format_last_update(last_update_seconds):
    min, sec = divmod(last_update_seconds, 60) 
    hour, min = divmod(min, 60)
    day, hour = divmod(hour, 24)
    if day > 0:
        return "%d days %d hours %d minutes %d seconds" % (day, hour, min, sec)
    elif hour > 0:
        return "%d hours %d minutes %d seconds" % (hour, min, sec)
    elif min > 0:
        return "%d minutes %d seconds" % (min, sec)
    else:
       return "%d seconds" % (sec)
  
def notify(type='info', msg=''):
    global notification
    
    if type == 'info':
      logging.info(msg)
      notification.append({'type': 'info', 'timestamp': datetime.now().strftime("%d %b %Y, %H:%M:%S"), 'text': msg})
    elif type == 'debug':
      logging.debug(msg)
    elif type == 'warning':
      logging.warning(msg)
      notification.append({'type': 'warning', 'timestamp': datetime.now().strftime("%d %b %Y, %H:%M:%S"), 'text': msg})
    elif type == 'success':
      logging.info(msg)
      notification.append({'type': 'success', 'timestamp': datetime.now().strftime("%d %b %Y, %H:%M:%S"), 'text': msg})
    elif type == 'error':
      logging.error(msg)  # TODO: maybe remove this line to be only as try/except with traceback?
      notification.append({'type': 'danger', 'timestamp': datetime.now().strftime("%d %b %Y, %H:%M:%S"), 'text': msg})
    else:
      print('notification type invalid!')

def update_dashboard_objects(system, weather):
    # Prepare data to send to website dict->json
    now = datetime.now()
    for id, plnt in enumerate(system.list_plants()):
        if plnt.get_last_update() != None:
            plants_dashboard[id].last_update = format_last_update(int((now - plnt.get_last_update()).total_seconds()))
            plants_dashboard[id].name = plnt.get_name()
            plants_dashboard[id].soil_moisture = plnt.get_health()
            
    for id, bat in enumerate(system.list_batteries()):
        if bat.get_last_update() != None:
            batteries_dashboard[id].last_update = format_last_update(int((now - bat.get_last_update()).total_seconds()))
            batteries_dashboard[id].level = bat.get_percentage()
            batteries_dashboard[id].state = bat.get_state()
            batteries_dashboard[id].errors = bat.list_errors() 

    for id, sect in enumerate(system.list_sectors()):
        if sect.get_last_update() != None:
            sectors_dashboard[id].last_update = format_last_update(int((now - sect.get_last_update()).total_seconds()))
            sectors_dashboard[id].watering = sect.is_watering()
            sectors_dashboard[id].plants = sect.list_plants()
            sectors_dashboard[id].errors = sect.list_errors()

    for id, wtrtnk in enumerate(system.list_watertanks()):
        if wtrtnk.get_last_update() != None:
            watertanks_dashboard[id].last_update = format_last_update(int((now - wtrtnk.get_last_update()).total_seconds()))
            if wtrtnk.is_valid():
                watertanks_dashboard[id].level = 100
                watertanks_dashboard[id].errors = ''
            else:
                watertanks_dashboard[id].level = 5
                watertanks_dashboard[id].errors = 'empty'
                
    if weather.get_current_weather()['last_update'] != None:
        weather_dashboard.city = weather.get_current_weather()['city']
        weather_dashboard.temperature = weather.get_current_weather()['temperature']
        weather_dashboard.real_feel = weather.get_current_weather()['real_feel']
        weather_dashboard.humidity = weather.get_current_weather()['humidity']
        weather_dashboard.description = weather.get_current_weather()['description']
        weather_dashboard.icon = weather.get_current_weather()['icon']
        weather_dashboard.last_update = format_last_update(int((now - weather.get_current_weather()['last_update']).total_seconds()))

    if weather.get_next_expected_rain()['last_update'] != None:
        next_rain_dashboard.city = weather.get_next_expected_rain()['city']
        next_rain_dashboard.time = weather.get_next_expected_rain()['time']
        next_rain_dashboard.real_feel = weather.get_next_expected_rain()['real_feel']
        next_rain_dashboard.description = weather.get_next_expected_rain()['description']
        next_rain_dashboard.icon = weather.get_next_expected_rain()['icon']
        next_rain_dashboard.rain = weather.get_next_expected_rain()['rain']
        next_rain_dashboard.last_update = format_last_update(int((now - weather.get_next_expected_rain()['last_update']).total_seconds()))
    

class OpenWeatherMap():
    def __init__(self, refresh_rate_s, city, weather_url, forecast_url):
        #__weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
        #__forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=63f4d3e36c7caad4496f47edcea1bd23'
        self.__weather_url = weather_url
        self.__forecast_url = forecast_url
        self.__forecast = None
        self.__city = city
        self.__is_running = True
        self.__refresh_rate_s = refresh_rate_s
        self.__rain_expected = False
        self.__current_weather = {
            'city': self.__city,
            'temperature': -273.15,
            'real_feel' : -273.15,
            'humidity' : 0,
            'description': 'unknown',
            'icon': '',
            'last_update': None
        }
        self.__forecast_3hr = {
            'city': self.__city,
            'time': '1990-01-01 00:00:00',
            'real_feel': -273.15,
            'description': 'unknown',
            'icon': '',
            'rain': 0,
            'last_update': None
        }
        self.__next_rain = {
            'city': self.__city,
            'time': '1990-01-01 00:00:00',
            'real_feel': -273.15,
            'description': 'unknown',
            'icon': '',
            'rain': 0,
            'last_update': None
            }

        def parse_data(self):

            try:
                curr = requests.get(weather_url.format(self.__city)).json()
                self.__forecast = requests.get(forecast_url.format(self.__city)).json()

                self.__current_weather = {
                    'city': __city,
                    'temperature': curr['main']['temp'],
                    'real_feel' : curr['main']['feels_like'],
                    'humidity' : curr['main']['humidity'],
                    'description': curr['weather'][0]['description'],
                    'icon': curr['weather'][0]['icon'],
                    'last_update': datetime.now()
                }

                self.__forecast_3hr = {
                    'city': __city,
                    'time': self.__forecast['list'][1]['dt_txt'],
                    'real_feel': self.__forecast['list'][1]['main']['feels_like'],
                    'description': self.__forecast['list'][1]['weather'][0]['description'],
                    'icon': self.__forecast['list'][1]['weather'][0]['icon'],
                    'rain': self.__forecast['list'][i]['weather'][0]['main'],
                    'last_update': datetime.now()
                }
                return True
            
            except:
                return False

        def find_next_expected_rain(self):
            for i in range(30):
                if self.__forecast['list'][i]['weather'][0]['main'] == 'Rain':
                    self.__next_rain['time'] = self.__forecast['list'][i]['dt_txt']
                    self.__next_rain['description'] = self.__forecast['list'][i]['weather'][0]['description']
                    self.__next_rain['icon'] = self.__forecast['list'][i]['weather'][0]['icon']
                    self.__next_rain['rain'] = self.__forecast['list'][i]['rain']['3h']
                    self.__next_rain['real_feel'] = self.__forecast['list'][i]['main']['feels_like']
                    self.__next_rain['last_update'] = datetime.now()
                    return True
                else:
                    return False
        
        def run(self):

            while self.__is_running:
                
                if self.parse_data():
                    if self.find_next_expected_rain():
                        self.__rain_expected = True
                    else:
                        self.__rain_expected = False
                    
                time.sleep(__refresh_rate_s)

        def terminate(self):
            self.__is_running = False

        def get_current_weather(self):
            return self.__current_weather

        def get_forecast_next3h(self):
            return self.__forecast_3hr

        def get_next_expected_rain(self):
            if self.__rain_expected:
                return self.__next_rain
            else:
                return {'city': self.__city, 'time': '0000-00-00 00:00:00', 'real_feel': -273.15, 'description': 'no rain expected in nearest future', 'icon': '', 'rain': 0, 'last_update': format_last_update(int((now - wtrtnk.get_last_update()).total_seconds()))}
            
    
def new_client(client, server):
    global notification_archive
    msg = json.dumps({'sectors': sectors_dashboard, 'plants': plants_dashboard, 'watertanks': watertanks_dashboard, 'power': batteries_dashboard, 'notifications': notification_archive, 'weather': weather_dashboard, 'next_rain': next_rain_dashboard})
    server.send_message(client, msg)
    print("new client: ", client['address']," joined")

def new_msg(client, server, message):
    global notification
    global notification_archive
    NOTIFICATION_ARCHIVE_LEN_MAX = 100
    global i
    i=i+1
    notify('success',str(i))
    
    msg = json.dumps({'sectors': sectors_dashboard, 'plants': plants_dashboard, 'watertanks': watertanks_dashboard, 'power': batteries_dashboard, 'notifications': notification, 'weather': weather_dashboard, 'next_rain': next_rain_dashboard})
    server.send_message_to_all(msg)
    
    notification_archive.extend(notification)
    notification_archive_overrun = len(notification_archive) - NOTIFICATION_ARCHIVE_LEN_MAX
    if notification_archive_overrun > 0:
      notification_archive = notification_archive[notification_archive_overrun:]
    notification = []
    print("new msg sent", i)

def client_left(client, server):
    print("client: ", client['address']," left")


if __name__ == "__main__":

  server = WebsocketServer(1234, host='127.0.0.1')
  server.set_fn_new_client(new_client)
  server.set_fn_message_received(new_msg)
  server.set_fn_client_left(client_left)

  server_thread = threading.Thread(name='website', target=server.run_forever)
  server_thread.daemon = True
  server_thread.start()

  try:
    while True:
      time.sleep(1)
      print(".")
  except KeyboardInterrupt:
    pass


#server.server_close()
#server_thread.join(5)
#del server_thread
#del server

print("shutting down...")
#sys.exit()
    


