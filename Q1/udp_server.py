#!/usr/bin/env python3

import sys
from socket import *

### Caso queira alterar essa porta lembre-se de altere tambem no client ###
PORT_UDP = 50003

s = socket(AF_INET,SOCK_DGRAM)
HOST = gethostbyname('0.0.0.0')
s.bind((HOST,PORT_UDP))

print("Servidor de echo inicializado.")

while True:
	msg, addr = s.recvfrom(1024)
	print ("Addr: ", addr)
	print ("Msg:  ", msg.decode('utf-8'))
	print ()
	s.sendto(msg, addr)
