import socket
import json
import time
from websocket_server import WebsocketServer
import threading


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

notification = []

notification1 = {'type': 'warning', 'timestamp': '202006301838', 'text': 'Just a simple warning'}
notification2 = {'type': 'success', 'timestamp': '202006301839', 'text': 'Just a simple success'}
notification3 = {'type': 'danger', 'timestamp': '202006301840', 'text': 'Just a simple danger'}
notification4 = {'type': 'info', 'timestamp': '202006301841', 'text': 'Just a simple info'}
notification.append(notification1)
notification.append(notification2)
notification.append(notification3)
notification.append(notification4)



def new_client(client, server):
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery, 'notifications': notification})
    server.send_message_to_all(msg)
    print("new client: ", client['address']," joined")

def new_msg(client, server, message):
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery, 'notifications': notification})
    server.send_message_to_all(msg)
    #clear notification after sending
    print("new msg sent")

def client_left(client, server):
    print("client: ", client['address']," left")



server = WebsocketServer(1234, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_message_received(new_msg)
server.set_fn_client_left(client_left)

server_thread = threading.Thread(name='server', target=server.run_forever)
server_thread.daemon = True
server_thread.start()


