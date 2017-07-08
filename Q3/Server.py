import socket
import random
import select

class Server:
    __playerList = []
    __serverSock = []

    def __init__(self, Ssock):
        self.__serverSock = Ssock
        print("Recebendo requisiçoes")

    def insert (self, addr):
        print("Requisicao recebida de ", addr)
        self.__playerList.append(addr)
        if len(self.__playerList) >= 2:
            p1 = self.__playerList.pop(0)
            p2 = self.__playerList.pop(0)
            choice = random.randint(0,1)
            self.__serverSock.sendto(str((p2,choice)).replace("(","").replace(")","").replace(" ","").encode(), p1)
            self.__serverSock.sendto(str((p1,(choice+1)%2)).replace("(","").replace(")","").replace(" ","").encode(), p2)
        else:
            self.__serverSock.sendto(b'Wait Opponent',addr)


random.seed(None)
HOST = ""
PORT = 50984
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST,PORT))
print("Servidor Inicializado")
Serv = Server(s)
while 1:
    ready_to_read, ready_to_write, in_error = select.select([s], [], [], 0)  # Checa se há pacotes no buff
    for sock in ready_to_read:  # se ready_to_read nao for uma lista vazia executa isso
        try:
            msg, addr = sock.recvfrom(1024)
            if msg == b'Get Game':
                Serv.insert(addr)
        except:
            pass
