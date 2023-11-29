import threading
import socket

HOST = "192.168.1.132"
PORT = int(input("Port: "))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def connect():
    while True:
        try:
            inp = input(">>>")
            client.send(bytes(inp, "utf-8"))
            print("Sent: ", inp)
        except (Exception, KeyboardInterrupt):
            break


def message():
    while True:
        msg = client.recv(1024)
        print("Received: ", msg.decode("utf-8"))


threading.Thread(target=connect).start()
threading.Thread(target=message).start()
