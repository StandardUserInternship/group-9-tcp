# server.py

import socket
import threading
import requests

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

userList = []

def on_new_client(conn,addr):

    print(f"Connected by {addr}")

    data = conn.recv(1024).decode('ascii')
    data.split(" ")
    userName = data[0]
    global userList
    userList.append(userName) 
 
    while True:
        data = conn.recv(1024).decode('ascii')
        if data == "!QUIT":
            break

        elif data == "!LIST":
            conn.send(userList)

        else:
            conn.sendall(data.encode('ascii'))

    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)

print ('Server started!')
print ('Waiting for clients...')

s.bind((HOST, PORT))        # Bind to the port
s.listen(5)   

while True:
   c, addr = s.accept()     # Establish connection with client.
   threading.start_new_thread(on_new_client,(c,addr))
  
   


