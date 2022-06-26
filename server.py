# server.py

import socket
import threading
import time

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
    for key in connDict:
            key.send(f"{userName} connected to server".encode())
    
 
    while True:
        data = conn.recv(1024).decode()
        print(userName + ": " + data)

        if data == "!QUIT":
            time.sleep(2)
            break

        if data == "!LIST":
            list = ""
            for key, value in connDict.items():
                list = list + str(value) + ", "
            list = list[:len(list)-2]
            conn.send(list.encode())
            continue

        if (data.startswith("!")):
            flag = False
            data = data.replace("!", "", 1)
            for key, val in connDict.items():
                if data.startswith(val):
                    data = data.split(" ",1)[1]
                    data = f"(whisper) {userName}: {data}"
                    key.send(data.encode())
                    flag = True
                    
            
            if flag == True:
                continue                

               
        data = userName + ": " + data
        for key in connDict:
            key.send(data.encode())

    conn.close()
    del connDict[conn]
    for key in connDict:
            key.send(f"{userName} disconnected".encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)

print ('Server started!')
print ('Waiting for clients...')

while True:
   c, addr = s.accept()     # Establish connection with client.
   x = threading.Thread(target=on_new_client, args=(c,addr))
   x.start()
  
   


