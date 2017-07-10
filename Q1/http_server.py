#!/usr/bin/env python3

import sys
from socket import *

### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_TCP = 30003

sock = socket(AF_INET, SOCK_STREAM)
HOST = gethostbyname('0.0.0.0')
sock.bind( (HOST, PORT_TCP) )
sock.listen(1)

text_response = """ 
HTTP/1.1    200 OK\r
Accept-Ranges:  bytes\r
Content-Length: 38\r
Connection: Keep-Alive\r
Content-Type:   text/plain;  charset=UTF-8\r
\r
Parabens aqui esta sua resposta HTTP!
"""

while True:

    print ('Aguardando uma conexao')
    connection, client_address = sock.accept()
    print ('Addr: ', client_address)

    while True:
        data = connection.recv(1024)
        print ('Msg:  ', data.decode('utf-8'))

        if data.decode('utf-8').upper().find('HTTP') > 0:
            if data.decode('utf-8').upper().find('GET') > 0:
                connection.sendall(text_response.encode('utf-8'))
        elif data:
            print("ERRO not HTTP GET\nFechando a conexao...")
            break
        else:
            print ('A conexao foi perdida', client_address)
            break
        
    print ()
    connection.close()