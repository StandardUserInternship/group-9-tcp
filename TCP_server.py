
import sys
import socket
import selectors


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 65432
handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (SERVER_ADDRESS, SERVER_PORT)
print(f'server {SERVER_ADDRESS} at port {SERVER_PORT}')

#sel = selectors.DefaultSelector()
users =[]
nicknames =[]


def main():
    print('server is connecting...')
    handler.bind(address)
    handler.listen()
    con = (handler.accept()[0])
    with con:
        print(' Connected ')
        #while True:
            #data = con.recv(4096)
            #if not data:
                #break
                #con.sendall(data)



main()


