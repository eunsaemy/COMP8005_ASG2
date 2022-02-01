#!/usr/bin/python

import socket
import ssl
import sys
from threading import Thread
import threading

# server host + port
SERVER_HOST = "192.168.0.12"
SERVER_PORT = 60000

# client1 host + port
HOST = "192.168.0.11"
PORT = 60002

# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# secure socket using SSL
client = ssl.wrap_socket(client, keyfile="./privkey.pem", certfile="./certificate.pem")

# receive messages
def recv():
    while True:
        # decode received messages
        data = client.recv(1024).decode()
        host = client.recv(1024).decode()
        port = client.recv(1024).decode()

        # host + port of received message
        recv_name = host + ':' + str(port)
        # host + port of current client
        curr_name = HOST + ':' + str(PORT)

        if not data:
            sys.exit(0)
        # echo received message if it's not from the current client
        elif recv_name != curr_name:
            print('[' + recv_name + '] ' + data)

# send messages
def send():
    while True:
        # request input from user
        send_data = input()

        # send input to server
        client.send(send_data.encode("utf-8"))

# main code
if __name__ == "__main__":
    # bind to socket
    client.bind((HOST, PORT))

    # connect to server
    client.connect((SERVER_HOST, SERVER_PORT))
    print("Connection successful")

    # start sending & receiving messages
    Thread(target=send).start()
    Thread(target=recv).start()
