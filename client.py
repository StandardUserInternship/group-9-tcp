# client.py

import socket
import threading
import argparse
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receive(s):
    while True:        
        data = s.recv(1024).decode()
        print("\n", data)

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
                s.send(f"{userName} disconnected".encode())
                print("Connection closed")
                s.close()
                sys.exit()
            
            elif (userInput.startswith("!HELP") or userInput.startswith("!help")):
                print("Useable commands:")
                print("<message>: Sends the message to all connected users")
                print("!LIST: display list of all users")
                print("!QUIT: quit chatting room")
                print("!<user name> <message>: send message to specific user")
            else :
                s.send(userInput.encode())
            

        
if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))