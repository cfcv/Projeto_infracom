import socket
import time
import select
delay = 10

class Game:

    def __init__(self, gui):
        self.__Opon = None
        self.__me = None
        self.__choice = -1
        self.__turn = 0
        self.__table = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.__myMove = (-1, -1)
        self.timer1 = 0
        self.timer2 = 0
        self.past = 0
        self.__timeState = True
        self.__gui = gui
        self.__icon = ""
        self.__opicon = ""

    def __isMyTurn(self) -> bool:
        if self.__choice == 0:
            if (self.__turn % 2) == 0:
                return True
            else:
                return False
        else:
            if (self.__turn % 2) == 0:
                return False
            else:
                return True

    def initSock(self):
        HOST = "localhost"
        PORT = 50984
        self.__me = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__me.sendto(b'Get Game', (HOST, PORT))
        return

    def connect(self, root):
        ret = self.__nbRecv()
        if type(ret) == type((1,2)):
            msg, addr = ret
            if msg == b'Wait Opponent':
                root.after(delay, lambda: self.connect(root))
                return
            else:
                Phost, Pport, choice = msg.decode().split(',')
                Pport = int(Pport)
                self.__choice = int(choice)
                if self.__choice == 0:
                    self.__icon = "X"
                    self.__opicon = "O"
                elif self.__choice == 1:
                    self.__icon = "O"
                    self.__opicon = "X"
                Phost = Phost.strip("'")
                print(Phost, str(Pport), str(choice))
                print("Jogador " + Phost + " " + str(Pport) + " Contactado")
                self.__me.sendto(b'Ola jogador', (Phost, Pport))
                root.after(delay, lambda: self.__waitConf(root))
                return
        root.after(delay, lambda: self.connect(root))
        return

    def __waitConf(self,root):  #Aguarda pela confirmação do oponente
        ret = self.__nbRecv()
        if type(ret) == type((1,2)):
            msg, addr = ret
            if msg == b'Ola jogador':
                self.__Opon = addr
                root.after(delay, lambda: self.run(root))
                self.__gui.info.configure(text = "Conectado")
                print("Jogador confirmou")
            else:
                root.after(delay, lambda: self.__waitConf(root))
        else:
            root.after(delay, lambda: self.__waitConf(root))
        return

    def __nbRecv(self):
        ready_to_read, ready_to_write, in_error = select.select([self.__me], [], [], 0)  # Checa se há pacotes no buff
        for sock in ready_to_read:  # se ready_to_read nao for uma lista vazia executa isso
            msg, addr = sock.recvfrom(1024)
            return (msg,addr)
        return None

    def __gameFinished(self):   #Checa cada linha, coluna e diagonal se algum jogador venceu.
        if (self.__table[0][0] == self.__table[0][1] == self.__table[0][2] != -1):
            if self.__table[0][0] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[1][0] == self.__table[1][1] == self.__table[1][2] != -1):
            if self.__table[1][0] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[2][0] == self.__table[2][1] == self.__table[2][2] != -1):
            if self.__table[2][0] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[0][0] == self.__table[1][0] == self.__table[2][0] != -1):
            if self.__table[0][0] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[0][1] == self.__table[1][1] == self.__table[2][1] != -1):
            if self.__table[0][1] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[0][2] == self.__table[1][2] == self.__table[2][2] != -1):
            if self.__table[0][2] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[0][0] == self.__table[1][1] == self.__table[2][2] != -1):
            if self.__table[0][0] == self.__choice:
                return 1
            else:
                return 2
        elif (self.__table[0][2] == self.__table[1][1] == self.__table[2][0] != -1):
            if self.__table[0][2] == self.__choice:
                return 1
            else:
                return 2
        else:
            for j in self.__table:
                if (-1) in j:
                    return 0
            return 3

    def __myTurn(self) -> None:  # Processa as mensagens necessárias no turno do jogador.
        self.past = time.perf_counter()
        if self.past - self.timer1 >= 5:      #Envia de 5 em 5 segundos uma comfirmação de que está conetado.
            self.__me.sendto(b'Connected', self.__Opon)
            self.timer1 = time.perf_counter() #E seta o timer inicial para o tempo atual.


    def sendPlay(self, i, j):
        if self.__isMyTurn():
            if (self.__table[i][j] == -1):    #Se jogada for válida, envia ao oponente
                self.__myMove = (i,j)
                self.__me.sendto(
                    (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn)).encode(),
                    self.__Opon)    #Envia jogada ao oponente
                self.__turn += 1    #Incrementa turno
                self.__timeState = True
                if self.__choice == 0:
                    self.__gui.buttons[i][j].configure(text="X")
                elif self.__choice == 1:
                    self.__gui.buttons[i][j].configure(text="O")
                self.__table[self.__myMove[0]][self.__myMove[1]] = self.__choice   #Salva jogada na tabela
                return True
        return False

    def __opTurn(self) -> None:
        self.past = time.perf_counter()
        if ((self.past - self.timer1) >= 20): #Se tiver passado 20 segundos sem nenhuma comunicação, desconeta.
            print("Jogador desconectado!")
            quit()
        ready_to_read, ready_to_write, in_error = select.select([self.__me], [], [], 0) #Checa se há pacotes no buff
        for sock in ready_to_read:              #se ready_to_read nao for uma lista vazia executa isso
            msg, addr = sock.recvfrom(1024)
            if msg.decode() == "Connected":     #Se mensagem for de confirmação de conexão:
                self.timer1 = self.timer2 = time.perf_counter() #-> atualiza timer
                print("Connected confirmed")
            else:                               #Caso contrário, lê jogada do adversário
                posX, posY, round = msg.decode().split(",")
                print("jogador: ", addr, " enviou pacote ", "(" + posX + "," + posY + "," + round + ")  ", self.__turn)
                round = int(round)
                posX = int(posX)
                posY = int(posY)
                if (addr == self.__Opon) and (round == self.__turn):
                    # Checa se o pacote vem do oponente e se tem o número de rodada correto.
                    # Se não for o correto, o pacote é duplicado, então é ignorado.
                    self.__turn += 1
                    self.__table[posX][posY] = (self.__choice + 1) % 2
                    self.__timeState = True
                    self.__gui.buttons[posX][posY].configure(text = self.__opicon)
                    print("Adversario colocou em: ", posX + 1, " ", posY + 1)
                    return

        if (self.__myMove != (-1, -1)) and ((self.past - self.timer2) >= 10):
            # Se tiver se passado 17 segundos, reenvia a jogada (assume que o adversário não recebeu sua jogada)
            self.timer2 = time.perf_counter()   #atualiza timer2
            print("reenviando")
            self.__me.sendto(
                (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn - 1)).encode(),
                self.__Opon)

    def run(self, root):
        x = self.__gameFinished()
        if (self.__timeState):
            self.timer1 = self.timer2 = time.perf_counter()
        if not (x):
            if self.__isMyTurn():
                self.__gui.info.configure(text="Sua vez.")
                self.__myTurn()
            else:
                self.__gui.info.configure(text="Aguarde oponente.")
                self.__opTurn()
        else:
            if x == 1:
                print("Voce Venceu")
                quit()
            elif x == 2:
                print("Voce Perdeu")
                quit()
            else:
                print("Deu velha")
                quit()
        self.__timeState = False
        root.after(delay, lambda: self.run(root))
        return
