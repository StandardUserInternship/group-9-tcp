# Create one file that is run multiple times to create multiple instances of a client. 
# See the client pictures at the end of the document for examples.
# This file should require a command line argument for a username in order to start.
# This file should automatically connect to the server if the server is running.

import sys
import selectors
import socket
import threading

#first client choose a nickname
nickname = input('Choose a nickname: ')

#define client and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

#define receive function
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

#define write function
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


#enable threading for muliti users. only one user at a time is recieved
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


