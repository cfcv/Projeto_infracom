#!/usr/bin/env python3

import sys
from socket import *

SERVER_IP = input('Digite o IP do servidor\n')
### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_NUMBER_SERVER = 50003


mySocket = socket( AF_INET, SOCK_DGRAM )
hostName = gethostbyname( '0.0.0.0' )


data = ""
while str(data).upper().find("SAIR") < 0:

    myMessage = input('Digite a msg e\\ou \"sair\" para sair\n')
    mySocket.sendto(myMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER_SERVER))
    print("...")

    (data,addr) = mySocket.recvfrom(1024)
    print (data.decode('utf-8'))
    print()

mySocket.sendto("saiu".encode('utf-8'),(SERVER_IP,PORT_NUMBER_SERVER))


