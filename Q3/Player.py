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
        self.__table = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def __gameFinished(self):
        if (self.__table[0][0] == self.__table[0][1] == self.__table[0][2] != -1) or (
                    self.__table[1][0] == self.__table[1][1] == self.__table[1][2] != -1) or (
                    self.__table[2][0] == self.__table[2][1] == self.__table[2][2] != -1):
            return True
        elif (self.__table[0][0] == self.__table[1][0] == self.__table[2][0] != -1) or (
                    self.__table[0][1] == self.__table[1][1] == self.__table[2][1] != -1) or (
                    self.__table[0][2] == self.__table[1][2] == self.__table[2][2] != -1):
            return True
        elif (self.__table[0][0] == self.__table[1][1] == self.__table[2][2] != -1) or (
                    self.__table[0][2] == self.__table[1][1] == self.__table[2][0] != -1):
            return True
        else:
            return False

    def __myTurn(self) -> None:
        print("Digite as coordenadas (1<=x<=3 e 1<=y<=3)")
        posX, posY = input().split(" ")
        posX = int(posX)-1
        posY = int(posY)-1
        #aqui fazemos um código que espera pela confirmação da jogada
        if (0<=posX<=2) and (0<=posY<=2):
            self.__me.sendto((str(posX)+","+str(posY)+","+str(self.__turn)).encode(),self.__Opon)
            while 1:
            # aqui fazemos um código que espera pela confirmação da jogada
        else
            print("Erro, variáveis erradas")
        return

    def __opTurn(self) -> None:
        while 1:
            msg, addr = self.__me.recvfrom(1024)
            if addr == self.__Opon:
                break
        posX, posY, round = msg.decode.split(",")
        if round == self.__turn:
            self.__turn += 1
            self.__table[posX][posY] = (choice+1)%2
            self.__me.sendto("OK".encode(),self.__Opon)
        return

    def run(self):
        while not (gameFinished()):
            if choice == 0:
                if (turn % 2) == 0:
                    self.__opTurn()
                else:
                    self.__myTurn()
            else:
                if (turn % 2) == 0:
                    self.__myTurn()
                else:
                    self.__opTurn()
        return


HOST = "localhost"
PORT = 50984
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Get Game', (HOST, PORT))
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
    s.sendto(b'Ola jogador', (Phost, Pport))
    msg, player = s.recvfrom(1024)
    if player == (Phost, Pport):
        jogo = Game(s, player, choice)
        print(msg.decode())
