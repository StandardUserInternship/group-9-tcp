# client.py

import socket
import threading
import argparse
import sys
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
stop_threads = False

def receive(s):
    global stop_threads
        
    while True: 
        if stop_threads:
            break
        data = s.recv(1024).decode()
        print("\n>>>", data)

def main(argv):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        userName = argv
        s.connect((HOST, PORT))
        s.sendall(f"{userName} entered to the chat room".encode())
        
        x = threading.Thread(target=receive, args=(s,))
        x.start()

        while True:
            userInput = str(input(f"{userName}: "))
            

            if (userInput.startswith("!LIST") or userInput.startswith("!list")):
                s.send('!LIST'.encode())

            elif (userInput.startswith("!QUIT") or userInput.startswith("!quit")):
                s.send("!QUIT".encode())
                print("Connection closed")
                global stop_threads
                stop_threads = True
                x.join()
                sys.exit()
            
            elif (userInput.startswith("!HELP") or userInput.startswith("!help")):
                print("Useable commands:")
                print("<message>: Sends the message to all connected users")
                print("!LIST: display list of all users")
                print("!QUIT: quit chatting room")
                print("!<user name> <message>: send message to specific user")
                print("!BLOCK <user name>: block user")
                print("!UNBLOCK <user name>: unblock user")
            else :
                s.send(userInput.encode())
            

        
if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))