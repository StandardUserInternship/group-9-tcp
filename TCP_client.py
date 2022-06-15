# Create one file that is run multiple times to create multiple instances of a client. 
# See the client pictures at the end of the document for examples.
# This file should require a command line argument for a username in order to start.
# This file should automatically connect to the server if the server is running.

import sys
import socket
import selectors


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 65432
address = (SERVER_ADDRESS, SERVER_PORT)
users =[]
nicknames =[]

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.send(b' handshake ')
    data = sock.recv(4096)
    print(f'received...  {data!r}')
    #while True:
        #data =sock.recv(4096)
        #if not data: break
        #sock.sedall(data)


# def receive():


# def write():
    #while True:



main()