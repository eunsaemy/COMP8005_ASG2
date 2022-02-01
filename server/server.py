# !/usr/bin/python

import socket
import ssl
import sys
from threading import Thread
import threading

# server host + port
HOST = "192.168.0.12"
PORT = 60000

# create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# secure socket using SSL
server = ssl.wrap_socket(
    server, server_side=True, keyfile="privkey.pem", certfile="certificate.pem"
)

# list of clients
clients = set()

# mutex (multi-threading)
clients_lock = threading.Lock()

# handle client
def clientthread(conn, addr):
    with clients_lock:
        clients.add(conn)
        
    try:
        while True:
            data = conn.recv(1024)
            host = addr[0].encode()
            port = str(addr[1]).encode()

            if not data:
                break
            # record chat session to a text file
            elif data.decode() == "FILE":
                f = open("chat.txt", "w")

                for h in history:
                    f.write(h + '\n')

                f.close()

                print('Message has been written to a txt file')
            # list all connected clients
            elif data.decode() == "LIST":
                print(threads)
            # echo text strings from each client to all other clients except the one that sent it
            else:
                msg = '[' + addr[0] + ':' + str(addr[1]) + '] ' + data.decode()
                print(msg)
                history.append(msg)

                with clients_lock:
                    for c in clients:
                        c.sendall(data)
                        c.sendall(host)
                        c.sendall(port)

    finally:
        with clients_lock:
            # remove disconnected client from the list
            threads.remove(addr[0] + ':' + str(addr[1]))
            # remove client from client list
            clients.remove(conn)
            # close client
            conn.close()

# main code
if __name__ == "__main__":
    # bind to socket
    try:
        server.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')

    # listen on port
    server.listen(0)
    print('Socket now listening')

    # list of threads
    th = []
    # list of messages
    history = []
    # list of connected clients
    threads = []

    while True:
        # accepts connection
        conn, addr = server.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        # add client name
        threads.append(addr[0] + ':' + str(addr[1]))
        # handle client
        th.append(Thread(target=clientthread, args=(conn,addr)).start())

    # close socket
    server.close()
