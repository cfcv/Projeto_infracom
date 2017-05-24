import socket
import time
import tkinter as tk


class Game:
    __me = []
    __Opon = []
    __choice = -1
    __turn = 0
    __table = []

    def __init__(self, me, op, choice):
        print("Oponente: ", op)
        self.__Opon = op
        self.__me = me
        self.__choice = choice
        self.__turn = 0
        self.__table = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.__myMove = (-1, -1)

    def __gameFinished(self):
        if (self.__table[0][0] == self.__table[0][1] == self.__table[0][2] != -1):
            if self.__table[0][0] == choice:
                return 1
            else:
                return 2
        elif (self.__table[1][0] == self.__table[1][1] == self.__table[1][2] != -1):
            if self.__table[1][0] == choice:
                return 1
            else:
                return 2
        elif (self.__table[2][0] == self.__table[2][1] == self.__table[2][2] != -1):
            if self.__table[2][0] == choice:
                return 1
            else:
                return 2
        elif (self.__table[0][0] == self.__table[1][0] == self.__table[2][0] != -1):
            if self.__table[0][0] == choice:
                return 1
            else:
                return 2
        elif (self.__table[0][1] == self.__table[1][1] == self.__table[2][1] != -1):
            if self.__table[0][1] == choice:
                return 1
            else:
                return 2
        elif (self.__table[0][2] == self.__table[1][2] == self.__table[2][2] != -1):
            if self.__table[0][2] == choice:
                return 1
            else:
                return 2
        elif (self.__table[0][0] == self.__table[1][1] == self.__table[2][2] != -1):
            if self.__table[0][0] == choice:
                return 1
            else:
                return 2
        elif (self.__table[0][2] == self.__table[1][1] == self.__table[2][0] != -1):
            if self.__table[0][2] == choice:
                return 1
            else:
                return 2
        else:
            for j in self.__table:
                if (-1) in j:
                    return 0
            return 3

    def __myTurn(self) -> None:  # Recebe a jogada do usuário e envia ao oponente.
        while 1:
            print("Digite as coordenadas 'x y' (1<=x<=3 e 1<=y<=3)")
            posX, posY = input().split(" ")
            self.__myMove = (int(posX) - 1, int(posY) - 1)
            if (0 <= self.__myMove[0] <= 2) and (0 <= self.__myMove[1] <= 2) and (
                self.__table[self.__myMove[0]][self.__myMove[1]] == -1):

                self.__me.sendto(
                    (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn)).encode(),
                    self.__Opon)
                self.__turn += 1
                self.__table[self.__myMove[0]][self.__myMove[1]] = choice
                return
            else:
                print("Erro, variáveis erradas")

    def __opTurn(self) -> None:
        iniT = time.perf_counter()
        while 1:
            past = time.perf_counter()
            msg, addr = self.__me.recvfrom(1024)
            posX, posY, round = msg.decode().split(",")
            print("jogador: ", addr, " enviou pacote ", "(" + posX + "," + posY + "," + round + ")  ", self.__turn)
            round = int(round)
            posX = int(posX)
            posY = int(posY)
            if (addr == self.__Opon) and (round == self.__turn):
                # Checa se o pacote vem do oponente e se tem o número de rodada correto.
                # Se não for o correto, o pacote é duplicado, então é ignorado.
                self.__turn += 1
                self.__table[posX][posY] = (choice + 1) % 2
                print("Adversario colocou em: ", posX + 1, " ", posY + 1)
                return
            if (self.__myMove != (-1, -1)) and (past - iniT >= 1):
                # Se tiver se passado 1 segundo, reenvia a jogada (assume que o adversário não recebeu sua jogada)
                print("reenviando")
                self.__me.sendto(
                    (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn - 1)).encode(),
                    self.__Opon)

    def run(self):
        while not (self.__gameFinished()):
            if self.__choice == 0:
                if (self.__turn % 2) == 0:
                    self.__opTurn()
                else:
                    self.__myTurn()
            else:
                if (self.__turn % 2) == 0:
                    self.__myTurn()
                else:
                    self.__opTurn()
        else:
            x = self.__gameFinished()
            if x == 1:
                print("Voce Venceu")
            elif x == 2:
                print("Voce eh um bosta")
            else:
                print("Deu velha")
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
        jogo.run()
        quit()
