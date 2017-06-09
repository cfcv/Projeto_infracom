#!/usr/bin/env python3

import sys
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import _thread
import time

# RXTX UDP
SERVER_IP   = '192.168.15.8'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
myMessage = "Say hello again, i dare you, i double dare you!"
myMessage1 = ""

hostName = gethostbyname( '0.0.0.0' )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

data = ""
while str(data).upper().find("UDP") < 0:
# while True:
    myMessage = input('type the service\n')
    mySocket.sendto(myMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))

    (data,addr) = mySocket.recvfrom(SIZE)
    print (data)

mySocket.sendto(myMessage1.encode('utf-8'),(SERVER_IP,PORT_NUMBER))


