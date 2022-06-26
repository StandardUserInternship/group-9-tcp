# server.py

import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

connDict = {}

def on_new_client(conn,addr):

    print(f"Connected by {addr}")

    data = conn.recv(1024).decode()
    print(data)
    data = data.split()
    userName = data[0]
    global connDict
    connDict[conn] = userName
    
 
    while True:
        data = conn.recv(1024).decode()
        if (data):
            print(data)

        if data == "!QUIT":
            break

        elif data == "!LIST":
            list = ""
            for key, value in connDict.items():
                list = list + str(value) + ", "
            list = list[:len(list)-2]
            conn.send(list.encode())

        else:
            conn.send(data.encode())

    conn.close()
    del connDict[conn]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)

print ('Server started!')
print ('Waiting for clients...')

while True:
   c, addr = s.accept()     # Establish connection with client.
   x = threading.Thread(target=on_new_client, args=(c,addr))
   x.start()
  
   


