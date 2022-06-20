
import sys
import select
import socket
import threading

#define address and port
SERVER_ADDRESS = '127.0.0.1' #local host
SERVER_PORT = 55555
#define the server and active it to listen for connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (SERVER_ADDRESS, SERVER_PORT)
server.bind(address)
server.listen()
print(f'server {SERVER_ADDRESS} at port {SERVER_PORT}')

#define empty client and nickname lists
clients =[]
nicknames =[]

#define broadcast function
def broadcast(message):
    for client in clients:
        client.send(message)

#define handle function
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat! '.encode('ascii'))
            nicknames.remove(nickname)
            break

#define receive function...this is main function
def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#execute main function
print('Server is Listening...')
receive()
