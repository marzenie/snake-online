import socket
import json
import curses
import threading
import sys
import time
import random
from functions.extensions import split_jsons

class SnakeGameClient:
    def __init__(self, stdscr):
        settings_file      = 'settings.json'
        self.settings      = json.load(open(settings_file))
        self.stdscr        = stdscr
        self.no_start_game = True
        self.key           = curses.KEY_RIGHT
        self.error         = {"error": False, "desc": ""}
        self.login_pass    = {"name": self.settings['name'], "password": self.settings['password']}
        self.colors        = ["COLOR_RED", "COLOR_GREEN", "COLOR_BLUE", "COLOR_MAGENTA", "COLOR_CYAN", "COLOR_WHITE", "COLOR_BLACK"]
        self.random_next_time = random.randint(3, 13) 
        
        for index, color in enumerate(self.colors):
            curses.init_pair(index+1, curses.COLOR_BLACK, getattr(curses, color))
        
        try:
            port = int(self.settings['port'])
        except:
            self.error = {"error": True, "desc": "[ERROR] Port must be number"}
            
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.settings['host'], port))
        except Exception as e:
            self.error = {"error": True, "desc": e}
            

    def start(self):
    
        self.send(json.dumps(self.login_pass))
        Start_message = "Press R to start game"
        while True:           
            try:
                message = json.loads(self.sock.recv(self.settings['header']).decode())
            except:
                sys.exit(1)
                
                
            if message and message.get('login', True):
                self.snake_id    = list(message.keys())[0]
                self.token       = message[self.snake_id].get('token')
                self.position    = message[self.snake_id].get('position')
                break
               

        self.game_state = {self.snake_id: self.position } 
        threading.Thread(target=self.receive_game_state, daemon=True).start()
        
        while self.no_start_game: # whait for start signal or||and send it
            try:

                if int(self.snake_id) == 0 and self.no_start_game == True:
                    self.stdscr.addstr(2, (curses.COLS - len(Start_message)) // 2, Start_message, curses.color_pair(3))
                    key = self.stdscr.getch()
                    
                    if key == ord('R'):
                        self.send(json.dumps({"start": True, "token": self.token}))
            except ConnectionResetError:
                print("Connection was reset. Exiting.")
                sys.exit(1)
                
        self.stdscr.clear()          
        while True:
            self.handle_input()
            self.send_game_state()
            self.update_display()
            time.sleep(0.01)

    def handle_input(self):
    
        allow_keys_list = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
        next_key = self.stdscr.getch()
        self.key = self.key if ((next_key == -1) or (next_key not in allow_keys_list)) else next_key

        if self.game_state[self.snake_id]:
            head = self.game_state[self.snake_id][0]
            new_head = [head[0], head[1]]

        if self.key == curses.KEY_DOWN and head[0] + 1 != self.game_state[self.snake_id][1][0]:
            new_head[0] += 1
        elif self.key == curses.KEY_UP and head[0] - 1 != self.game_state[self.snake_id][1][0]:
            new_head[0] -= 1
        elif self.key == curses.KEY_LEFT and head[1] - 1 != self.game_state[self.snake_id][1][1]:
            new_head[1] -= 1
        elif self.key == curses.KEY_RIGHT and head[1] + 1 != self.game_state[self.snake_id][1][1]:
            new_head[1] += 1

        self.game_state[self.snake_id].insert(0, new_head)  # Update the snake's position
        self.game_state[self.snake_id].pop()  # Remove the tail segment

    def send_game_state(self):
        self.send(json.dumps(self.game_state))
        
    def send(self, message):
        self.sock.send(message.encode())
        

    
    def receive_game_state(self):
        def get_update(self, msg):
            if msg:
                if msg.get('update') == True:
                    for key in msg.keys():
                        if key == "update":
                            continue
                        self.game_state[key] = msg.get(key)
                if ((msg.get('join') == True) and (self.no_start_game == True)):
                    print(msg['desc'])
                if msg.get('start') == True:
                    self.no_start_game = False
        while True:
            try:
                msg = json.loads(self.sock.recv(self.settings['header']).decode())
                get_update(self, msg)
            except ConnectionResetError:
                break
            except:
                split_js = split_jsons(msg)

                for json_str in split_js:
                    get_update(self, json_str)

    def check_collision(self, snake):
        #cell_ch = window.inch(snake[0], snake[1]) & curses.A_CHARTEXT
        colors_array = [0, 67108864, 1024, 1792]
        cell_color = self.stdscr.inch(snake[0], snake[1]) & curses.A_COLOR
        if cell_color in colors_array:
            return False
        return True
        
    def empty_space(self):
        if self.random_next_time == 1:
            if 1 == random.randint(0, 1):
                return False
            self.random_next_time  = random.randint(31, 94)
            return True
        self.random_next_time  -= 1
        return False
    
    def update_display(self):
        empty_spc = self.empty_space()
        for key in self.game_state.keys():
            if key == "update":
                continue
                
            snake = self.game_state[key]
            for i, (y, x) in enumerate(snake):
                if i == 0:
                    yx = [y, x]
                    if (self.check_collision(yx) == True and (empty_spc == False)):
                            # server end com & koniec do spania dla pana
                            sys.exit(1)
                    else:
                        self.stdscr.addch(y, x, '•', curses.color_pair(6))
                elif i == 1:
                    if (empty_spc == True):
                        self.stdscr.addch(y, x, ' ', curses.color_pair(7))
                    elif (snake[2][0] == snake[1][0]) and (snake[0][0] > snake[1][0]): #lewo dół, prawo dół
                        if (snake[2][1] < snake[1][1]):
                            self.stdscr.addch(y, x, '┓', curses.color_pair(int(key)+1))
                        else:
                            self.stdscr.addch(y, x, '┏', curses.color_pair(int(key)+1))
                            
                    elif (snake[2][0] == snake[1][0]) and (snake[0][0] < snake[1][0]):  # prawo góra, lewo góra  
                        if (snake[2][1] < snake[1][1]):
                            self.stdscr.addch(y, x, '┛', curses.color_pair(int(key)+1))
                        else:
                            self.stdscr.addch(y, x, '┗', curses.color_pair(int(key)+1))
                            
                    elif (snake[2][0] > snake[1][0]) and (snake[0][0] == snake[1][0]):  # góra prawo, góra lewo    
                        if (snake[0][1] < snake[1][1]):
                            self.stdscr.addch(y, x, '┓', curses.color_pair(int(key)+1))
                        else:
                            self.stdscr.addch(y, x, '┏', curses.color_pair(int(key)+1))
                            
                    elif (snake[2][0] < snake[1][0]) and (snake[0][0] == snake[1][0]):  # dół prawo, dół lewo    
                        if (snake[0][1] < snake[1][1]):
                            self.stdscr.addch(y, x, '┛', curses.color_pair(int(key)+1))
                        else:
                            self.stdscr.addch(y, x, '┗', curses.color_pair(int(key)+1))
                            
                    elif snake[1][0] == snake[0][0]:
                        self.stdscr.addch(y, x, '━', curses.color_pair(int(key)+1))
                    elif snake[1][1] == snake[0][1]:
                        self.stdscr.addch(y, x, '┃', curses.color_pair(int(key)+1)) #━┃┏┓┗┛
                    
def game(stdscr):
    # Curses initialization
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.start_color()

    # Start the game client
    client = SnakeGameClient(stdscr)
    if client.error['error']:
        return client.error
    client.start()
