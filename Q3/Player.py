import socket

class Game:
    __me = []
    __Opon = []
    __choice = -1
    __turn = 0
    __table = []

    def __init__(self, me, op, choice):
        self.__Opon = op
        self.__me = me
        self.__choice = choice
        self.__turn = 0
        self.__table = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]

    #def __gameFinished (self):
    #    if (self.__table[0][0] == self.__table[0][1] == self.__table[0][2]!= -1) || (self.__table[1][0] == self.__table[1][1] == self.__table[1][2]!= -1) || (self.__table[2][0] == self.__table[2][1] == self.__table[2][2]!= -1):
    #        return True
    #    if (self.__table[0][0] == self.__table[1][0] == self.__table[2][0]!= -1) || (self.__table[0][1] == self.__table[1][1] == self.__table[2][1]!= -1) || (self.__table[0][2] == self.__table[1][2] == self.__table[2][2]!= -1):
    #        return  True
    #    if (self.__table[0][0] == self.__table[1][1] == self.__table[2][2] != -1) || (self.__table[0][2] == self.__table[1][1] == self.__table[2][0]!= -1):
    #        return True
    #     else:
    #        return False

    def __myTurn (self):


    def __opTurn (self):
        while 1:
            msg, addr = self.__me.recvfrom(1024)
            if addr == self.__Opon:
                break
        posX, posY = msg.decode.split(",")
        #modifica jogo
        self.__turn += 1



    def run (self):
        while not(gameFinished()):
         if choice == 0:
                if (turn%2) == 0:
                    self.__opTurn()
                else:
                    self.__myTurn()
            else:
                if (turn%2) == 0:
                    self.__myTurn()
                else:
                    self.__opTurn()


HOST = "localhost"
PORT = 5984
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(b'Get Game',(HOST,PORT))
while 1:
    msg, serv = s.recvfrom(1024)
    while msg == b'Wait Opponent':
        msg, serv = s.recvfrom(1024)
    Phost, Pport, choice = msg.decode().split(',')
    Pport = int(Pport)
    choice = int(choice)
    Phost = Phost.strip("'")
    print(Phost, str(Pport), str(choice))
    print("Jogador " + Phost + " " + str(Pport) + " Conectado")
    s.sendto(b'Ola jogador',(Phost,Pport))
    msg, player = s.recvfrom(1024)
    if player == (Phost,Pport):
        jogo = Game(s,player, choice)
        print(msg.decode())