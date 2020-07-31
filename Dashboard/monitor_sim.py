import socket
import json
import time
from websocket_server import WebsocketServer
import threading
import logging
from datetime import datetime
import sys


logging.basicConfig(filename='irrigation.log', filemode='w', format='%(asctime)s-%(levelname)s-%(process)d-%(message)s', level=logging.INFO)

try:
  c = 5 / 0
except Exception as e:
    logging.error(e, exc_info=True)


sector = [{
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

watertank = [{
    'type': 'tank',
    'last_update': '10min',
    'level': 50,
    'errors':''
    }]

battery = [{
    'type': 'power',
    'last_update': '14s',
    'level': 91,
    'state': 'charging',
    'errors': 'overvoltage'
    }]

plant = [{
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

def update_dicts(system):
    # Prepare data to send to website dict->json
    now = datetime.now()
    for id, plnt in enumerate(system.list_plants()):
        if plnt.get_last_update() != None:
            plant[id].last_update = format_last_update(int((now - plnt.get_last_update()).total_seconds()))
            plant[id].name = plnt.get_name()
            plant[id].soil_moisture = plnt.get_health()
        #print(plant.get_last_update(), plant.get_type(), plant.get_id(), "name:", plant.get_name(), "health:", plant.get_health())
    for id, bat in enumerate(system.list_batteries()):
        if bat.get_last_update() != None:
            battery[id].last_update = format_last_update(int((now - bat.get_last_update()).total_seconds()))
            battery[id].level = bat.get_percentage()
            battery[id].state = bat.get_state()
            battery[id].errors = bat.list_errors() 
        #print(battery.get_last_update(), battery.get_type(), battery.get_id(), battery.get_percentage(), "%", battery.get_state(), "errors:", battery.list_errors())
    for id, sect in enumerate(system.list_sectors()):
        if sect.get_last_update() != None:
            sector[id].last_update = format_last_update(int((now - sect.get_last_update()).total_seconds()))
            sector[id].watering = is_watering()
            sector[id].plants = list_plants()
            sector[id].errors = list_errors()
        #print(sector.get_last_update(), sector.get_type(), sector.get_id(), "watering:", sector.is_watering(), "plants:", sector.list_plants(), "errors:", sector.list_errors())
    for id, wtrtnk in enumerate(system.list_watertanks()):
        if wtrtnk.get_last_update() != None:
            watertank[id].last_update = format_last_update(int((now - wtrtnk.get_last_update()).total_seconds()))
            if wtrtnk.is_valid():
                watertank[id].level = 100
                watertank[id].errors = ''
            else:
                watertank[id].level = 5
                watertank[id].errors = 'empty'
        #print(watertank.get_last_update(), watertank.get_type(), watertank.get_id(), "valid:", watertank.is_valid())

def new_client(client, server):
    global notification_archive
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery, 'notifications': notification_archive})
    server.send_message(client, msg)
    print("new client: ", client['address']," joined")

def new_msg(client, server, message):
    global notification
    global notification_archive
    NOTIFICATION_ARCHIVE_LEN_MAX = 100
    global i
    i=i+1
    notify('success',str(i))
    
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery, 'notifications': notification})
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
    


