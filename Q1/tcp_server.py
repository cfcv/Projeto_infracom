#!/usr/bin/env python3

import sys
from socket import *

### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_TCP = 10003

sock = socket(AF_INET, SOCK_STREAM)
HOST = gethostbyname('0.0.0.0')
sock.bind( (HOST, PORT_TCP) )
sock.listen(5)

while True:

    print ('Aguardando uma conexao')
    connection, client_address = sock.accept()

    print ('Addr: ', client_address)

    while True:
        data = connection.recv(1024)
        print ('Msg:  ', data.decode('utf-8'))

        if data:
            connection.sendall(data)
        else:
            print ('A conexao foi perdida', client_address)
            break
        
    print ()
    connection.close()