#!/usr/bin/env python3

import sys
from socket import *

### Coloque o IP do seu servidor aqui ###
SERVER_IP   = '192.168.25.96'
### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_NUMBER_SERVER = 10003


sock = socket(AF_INET, SOCK_STREAM)
sock.connect( (SERVER_IP, PORT_NUMBER_SERVER) )

message = ""
while str(message).upper().find("SAIR") < 0:
    # Enviando
    message = input('Digite a msg e\\ou \"sair\" para sair\n')
    sock.sendall(message.encode('utf-8'))

    # Wait for it...
    print("...")

    # Caso a resposta venha fragmentada
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        message = sock.recv(1024)
        amount_received += len(message)
        print (message.decode('utf-8'))

print ('Fechando o socket')
sock.close()

