import socket
import json
import time
from websocket_server import WebsocketServer


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
    'level': 10,
    'errors':''
    }]

battery = [{
    'type': 'power',
    'last_update': '10s',
    'level': 90,
    'state': 'undetermined',
    'errors': ''
    }]

plant = [{
    'type':'plant',
    'last_update': '10s',
    'name': '',
    'soil_moisture': 10
    },
    {
    'type':'plant',
    'last_update': '10s',
    'name': '',
    'soil_moisture': 10
    },
    {
    'type':'plant',
    'last_update': '10s',
    'name': '',
    'soil_moisture': 10
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    },
    {
    'type':'plant',
    'last_update': None,
    'name': '',
    'soil_moisture': 0
    }]



def new_client(client, server):
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery})
    server.send_message_to_all(msg)
    print("new client: ", client['address']," joined")

def new_msg(client, server, message):
    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery})
    server.send_message_to_all(msg)
    print("new msg sent")

def client_left(client, server):
    print("client: ", client['address']," left")



server = WebsocketServer(1234, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_message_received(new_msg)
server.set_fn_client_left(client_left)
server.run_forever()


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print('binding')
#s.bind((socket.gethostname(),1234))
#s.listen(5)
#print('1')


#while True:
#    clientsocket, address = s.accept()
#    print(clientsocket, address)
#    print("Connection from ", address, "has been established")
#    msg = json.dumps({'sectors': sector, 'plants': plant, 'watertanks': watertank, 'power': battery})
#    msg = '{:<4}'.format(str(len(msg))) + msg   
#    clientsocket.send(bytes('hello', "utf-8"))
#    clientsocket.close()


