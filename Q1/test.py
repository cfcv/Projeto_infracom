# RXTX UDP
from socket import socket,gethostbyname, AF_INET,SOCK_DGRAM
SERVER_IP   = '192.168.15.11'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
myMessage = "Hello!"
myMessage1 = ""

hostName = gethostbyname( '0.0.0.0' )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

while True:
    (data,addr) = mySocket.recvfrom(SIZE)
    print (data)
    myMessage = input()
    mySocket.sendto(myMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))


mySocket.sendto(myMessage1.encode('utf-8'),(SERVER_IP,PORT_NUMBER))