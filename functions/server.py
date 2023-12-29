import socket
import threading
import json
import sys
import queue
import random
from functions.extensions import generate_random

class GameServer:
    def __init__(self):
        
        settings_file = 'settings.json'
        self.settings = json.load(open(settings_file))
        self.error = {"error": False, "desc": ""}
        self.start = False
        self.players = []
        self.clients = []
        self.game_state = {"update": True}
        
        try:
            port = int(self.settings['port'])
        except ValueError:
            self.error = {"error": True, "desc": "[ERROR] Port must be number"}
            
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.settings['host'], port))
            self.server_socket.listen()
                 
        except OverflowError as oe:
            self.error = {"error": True, "desc": "[ERROR] Port number out of range"}
        except Exception as e:
            self.error = {"error": True, "desc": e}
    def start_s(self, output_queue):
        output_queue.put(self.error)
        print("Server started. Waiting for connections...")
        while len(self.players) < 5:
            client_socket, addr = self.server_socket.accept()
            
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(self.settings['header']).decode()
                if msg:
                    msg = json.loads(msg)
                    if self.start == True:
                        self.update_game_state(msg)
                        self.broadcast_game_state()
                    elif msg.get('name') and msg.get('password') == self.settings['password']:
                        random_pos_y = random.randint(5, 40)
                        random_pos_x = random.randint(5, 40)
                        if random.randint(0, 1) == 0:
                            random_start = [[random_pos_y, random_pos_x], [random_pos_y, random_pos_x-1], [random_pos_y, random_pos_x-2]]
                        else:
                            random_start = [[random_pos_y, random_pos_x], [random_pos_y-1, random_pos_x], [random_pos_y-2, random_pos_x]]
                        p_id = len(self.players)
                        player_object = {
                            p_id: {
                                "login": True,
                                "token": generate_random(16),
                                "position": random_start
                            }
                        }
                        self.game_state[p_id] = random_start          
                        self.players.append(player_object)
                        
                        client_socket.send(json.dumps(player_object).encode())
                        self.broadcast(json.dumps({"join": True, "desc": "[" + str(len(self.players)) + "] " + msg.get('name') + " joined the game"})) 
                    elif msg.get('name') and msg.get('password') != self.settings.get('password'):
                        client_socket.send(json.dumps({"login": False}).encode())
                    elif msg.get('start') and msg.get('token') == player_object[0]['token']:
                        self.start = True
                        self.broadcast(json.dumps({"start": True}))
                        
            except ConnectionResetError:
                break

    def update_game_state(self, client_update):

        client_update['update'] = True
        self.game_state = client_update

    def broadcast_game_state(self):
    
        for client in self.clients:
            client.send(json.dumps(self.game_state).encode())
    def broadcast(self, message):
        for client in self.clients:
            client.send(message.encode())
            
def start_server(output_queue):
    server = GameServer()
    if server.error['error']:
        output_queue.put(server.error)
        return 1
    
    server.start_s(output_queue)