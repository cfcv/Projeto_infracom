#!/usr/bin/env python3

import sys
from socket import *

SERVER_IP = input('Digite o IP do servidor\n')
### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_NUMBER_SERVER = 30003


sock = socket(AF_INET, SOCK_STREAM)
sock.connect( (SERVER_IP, PORT_NUMBER_SERVER) )
print("Conexao estabelecida\n")

message = """   
GET   /   HTTP/1.1\r
Host:   """ + SERVER_IP + """\r
Accept: text/plain\r
Connection: keep-alive\r
"""
print("Enviando o GET")
print("---------------------------------------------")

## Enviando o GET
sock.sendall(message.encode('utf-8'))

## Recebendo a resposta
amount_received = 0
amount_expected = len(message)
is_http = False
# Caso a resposta venha fragmentada
while amount_received < amount_expected:
    message = sock.recv(1024)
    amount_received += len(message)
    
    # Checking for HTTP answer
    if message.decode('utf-8').upper().find('HTTP') > 0:
        is_http = True
    else:
        break

    if is_http:
        print (message.decode('utf-8'))

print ('Fechando o socket')
sock.close()
