# server.py

import socket
import threading
import sys
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

connDict = {}

def on_new_client(conn,addr):

    print(f"Connected by {addr}")

    # initialize new user (constructor)
    data = conn.recv(1024).decode()
    print(data)
    data = data.split()
    userName = data[0]
    global connDict
    connDict[conn] = userName
    blockList = []

    # send users who entered
    for key in connDict:
            key.send(f"{userName} connected to server".encode())
    


    # command lists
    while True:
        data = conn.recv(1024).decode()
        print(userName + ": " + data)

        if data == "!QUIT":
            connDict.pop(conn)
            for key in connDict:
                key.send(f"{userName} disconnected".encode())
            conn.close()
            sys.exit()

        if data == "!LIST":
            list = ""
            for key, value in connDict.items():
                list = list + str(value) + ", "
            list = list[:len(list)-2]
            conn.send(list.encode())
            continue

        # block # - # -# - # -# - # -# - # -# - # -# - # -# - # -# - # 
        if (data.startswith("!BLOCK") or data.startswith("!block")):
            flag2 = False
            data = data.split(" ")

            for key, val in connDict.items():
                if (val == data[1]):
                    if(data[1] in blockList):
                        conn.send(f"{data[1]} is already blocked".encode())
                        flag2 = True
                        continue
                    blockList.append(data[1])
                    conn.send(f"{data[1]} blocked".encode())
                    flag2 = True
                
            if flag2 == True:
                continue

            conn.send(f"{data[1]} not founded".encode())
            continue   
        # - # -# - # -# - # -# - # -# - # -# - # -# - # -# - # 


        # unblock # - # -# - # -# - # -# - # -# - # -# - # -#
        if (data.startswith("!UNBLOCK") or data.startswith("!unblock")):
            flag3 = False
            data = data.split(" ")

            for key in blockList:
                if (key == data[1]):
                    blockList.remove(data[1])
                    conn.send(f"{data[1]} unblocked".encode())
                    flag3 = True
                
            if flag3 == True:
                continue

            conn.send(f"{data[1]} not founded in blocklist".encode())
            continue
        # - # - # -# - # -# - # -# - # -# - # -# - # -# - # -# - # -


        # whisper # - # -# - # -# - # -# - # -# - # -# - # -# - # 
        if (data.startswith("!")):
            flag1 = False
            data = data.replace("!", "", 1)
            for key, val in connDict.items():
                if data.startswith(val):
                    data = data.split(" ",1)[1]
                    data = f"(whisper) {userName}: {data}"
                    key.send(data.encode())
                    flag = True
                    
            
            continue 
        # - # -# - # -# - # -# - # -# - # -# - # -# - # -# - # 
        
        
        # default (public messgae)  // send to only unblocked users
        data = userName + ": " + data
        for key, val in connDict.items():
            if(val not in blockList):
                key.send(data.encode()) 
        
        # - # -# - # -# - # -# - # -# - # 

   
# main
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)

print ('Server started!')
print ('Waiting for clients...')

while True:
   c, addr = s.accept()     # Establish connection with client.
   x = threading.Thread(target=on_new_client, args=(c,addr))
   x.start()
  
   


