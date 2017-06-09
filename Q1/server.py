import socket

SERVER_IP = '192.168.15.11'

PORT_UDP = 50000
PORT_TCP = 50001
PORT_HTTP = 50002
HOST = gethostbyname('0.0.0.0')

s0 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s0.bind((HOST,PORT_HTTP))
s1.bind((HOST,PORT_UDP))
s2.bind((HOST,PORT_TCP))
print("Servidor inicializado.")

while True:
	msg, addr = s.recvfrom(1024)
	print "Msg: ",msg