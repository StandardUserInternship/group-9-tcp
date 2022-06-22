# client.py

import socket
import threading
import argparse
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receive(s):
    while True:
        data = s.recv(1024).decode('ascii')
        print(data)

def main(argv):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        userName = argv
        s.connect((HOST, PORT))
        s.sendall(f"{userName} entered to the chat room".encode('ascii'))
        
        threading.start_new_thread(receive,(s))

        while True:
            userInput = str(input())

            if (userInput.startswith('!LIST' or '!list')):
                s.send('list').encode('ascii')

            elif (userInput.startswith('!QUIT'or '!quit')):
                s.send(f"{userName} disconnected")
            
            elif (userInput.startswith('!HELP'or '!help')):
                print("Useable commands:")
                print("<message>: Sends the message to all connected users")
                print("!LIST: display list of all users")
                print("!QUIT: quit chatting room")
            else :
                s.send(userInput)
            

            s.sendall(userInput)
        
if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))