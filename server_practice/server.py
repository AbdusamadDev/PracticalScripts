import threading
import socket
import random

MAX_CONNECTIONS = 10

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    try:
        port = random.randint(1000, 9999)
        conn.bind(("0.0.0.0", port))
        conn.listen(MAX_CONNECTIONS)
        print(f"Connection established at port: {port}")
    except OSError:
        connect()


clients = {}


def ear():
    while True:
        try:
            client, addr = conn.accept()
            print("Current clients: ", clients)
            if client:
                clients[addr] = client
                print('New client is connected to server with address of: ', addr)
                messaging_engine = threading.Thread(target=messaging, args=(client, addr))
                print(f"Client: {client} connected")
                messaging_engine.start()
        except Exception as error:
            print("[ERROR]: ", error)
            break


def broadcast(message):
    for cl in clients.values():
        print(f"Sending message to {cl}")
        cl.send(message)


def messaging(client, addr):
    while True:
        try:
            message = client.recv(1024)
            if addr != client.getsockname()[0]:
                print(message.decode('utf-8'))
                broadcast(message=message)
        except Exception as error:
            print("[ERROR]: ", error)
            client.close()
            break


connect()
server_ear = threading.Thread(target=ear, args=tuple())
server_ear.start()

if __name__ == '__main__':
    print("Server started at localhost")
