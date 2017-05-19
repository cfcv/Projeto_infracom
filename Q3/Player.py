import socket
import time


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
        self.__myMove = (-1, -1)

    def __gameFinished(self):  # A função ainda não retorna que jogador é o vencedor, apenas se o jogo acabou
        if (self.__table[0][0] == self.__table[0][1] == self.__table[0][2] != -1) or (
                            self.__table[1][0] == self.__table[1][1] == self.__table[1][2] != -1) or (
                            self.__table[2][0] == self.__table[2][1] == self.__table[2][2] != -1):
            # verifica se alguma coluna foi preenchida por apenas x ou apenas o
            return True
        elif (self.__table[0][0] == self.__table[1][0] == self.__table[2][0] != -1) or (
                            self.__table[0][1] == self.__table[1][1] == self.__table[2][1] != -1) or (
                            self.__table[0][2] == self.__table[1][2] == self.__table[2][2] != -1):
            # verifica se alguma linha foi preenchida por apenas x ou apenas o
            return True
        elif (self.__table[0][0] == self.__table[1][1] == self.__table[2][2] != -1) or (
                            self.__table[0][2] == self.__table[1][1] == self.__table[2][0] != -1):
            # verifica as diagonais
            return True
        else:
            return False

    def __myTurn(self) -> None: # Recebe a jogada do usuário e envia ao oponente. (ainda simples, não checa se
        # posição já está sendo usada)
        print("Digite as coordenadas (1<=x<=3 e 1<=y<=3)")
        posX, posY = input().split(" ")
        self.__myMove = (int(posX) - 1, int(posY) - 1)
        if (0 <= posX <= 2) and (0 <= posY <= 2):
            self.__me.sendto((str(myMove[0]) + "," + str(myMove[1]) + "," + str(self.__turn)).encode(), self.__Opon)
            self.__turn += 1

        else
            print("Erro, variáveis erradas")
        return

    def __opTurn(self) -> None:
        iniT = time.perf_counter()
        while 1:
            past = time.perf_counter()
            msg, addr = self.__me.recvfrom(1024)
            posX, posY, round = msg.decode.split(",")
            if (addr == self.__Opon) and (round == self.__turn):
                # Checa se o pacote vem do oponente e se tem o número de rodada correto.
                # Se não for o correto, o pacote é duplicado, então é ignorado.
                self.__turn += 1
                self.__table[posX][posY] = (choice + 1) % 2
                break
            if (self.__myMove != (-1, -1)) and (iniT - past >= 1):
                # Se tiver se passado 1 segundo, reenvia a jogada (assume que o adversário não recebeu sua jogada)
                self.__me.sendto((str(myMove[0]) + "," + str(myMove[1]) + "," + str(self.__turn - 1)).encode(),
                                 self.__Opon)
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
