import time
import socket

HOST = "0.0.0.0"
PORT = 1111

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
while True:
    inp = input(">>>")
    client.send(bytes(inp, "utf-8"))
    print("Sent: ", inp)
