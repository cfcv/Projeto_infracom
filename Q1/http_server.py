#!/usr/bin/env python3

import sys
from socket import *

### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_TCP = 10003

sock = socket(AF_INET, SOCK_STREAM)
HOST = gethostbyname('0.0.0.0')
sock.bind( (HOST, PORT_TCP) )
# O numero maximo de conexoes possivel não passa de 1 pois em nosso codigo ao
# se conectar o servidor fica 'preso' na conexao com aquele cliente.
sock.listen(1)

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