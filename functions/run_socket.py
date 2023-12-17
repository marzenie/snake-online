import json
import socket
import threading
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(64).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
        conn.send("Msg received".encode(FORMAT))

    conn.close()
    
def run_socket():
    settings_file = 'settings.json'
    settings = json.load(open(settings_file))
    
    try:
        port = int(settings['port'])
    except:
        print("[ERROR] Port must be number")
        return 1
        

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((settings['host'], port))
        server.listen()
        print(f"[LISTENING] Server is listening on {settings['host']}:{port}")
        

    except OverflowError as oe:
        print(f"[ERROR] Port number out of range: {oe}")
        return 1
    except Exception as e:
        print("[ERROR] An exception occurred", e)
        return 1
        

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

