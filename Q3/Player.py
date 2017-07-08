import socket
import time
import select
delay = 10
delay2 = 2000
HOST = "192.168.0.8"
PORT = 50984

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
        """ Retorna True se for seu turno, False caso contrário """
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
        """ Inicialza o socket do jogador. """
        self.__me = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__me.sendto(b'Get Game', (HOST, PORT))
        return

    def connect(self):
        """ Recebe o endereço do adversário selecionado pelo servidor """
        ret = self.__nbRecv()
        if type(ret) == type((1,2)):
            msg, addr = ret
            if msg != b'Ola jogador' and msg != b'Wait Opponent':
                print(msg.decode())
                Phost, Pport, choice = msg.decode().split(',')
                Pport = int(Pport)
                self.__choice = int(choice)
                if self.__choice == 0:      # Seta os ícones de cada jogador.
                    self.__icon = "X"
                    self.__opicon = "O"
                elif self.__choice == 1:
                    self.__icon = "O"
                    self.__opicon = "X"
                Phost = Phost.strip("'")
                print(Phost, str(Pport), str(choice))
                print("Jogador " + Phost + " " + str(Pport) + " Contactado")
                self.__me.sendto(b'Ola jogador', (Phost, Pport))    #
                self.timer1 = time.perf_counter()
                self.__gui.root.after(delay, self.__waitConf)
                return
        self.__gui.root.after(delay, self.connect)
        return

    def __waitConf(self):  #Aguarda pela confirmação do oponente
        """ Aguarda confirmação do jogador enviado pelo servidor.
         Reenvia requisição ao servidor caso o jogador não responda a tempo ou esteja inalcançável pela rede."""
        ret = self.__nbRecv()
        if type(ret) == type((1,2)):
            msg, addr = ret
            if msg == b'Ola jogador':
                self.__Opon = addr
                self.__gui.root.after(delay, self.run)
                self.__gui.info.configure(text = "Conectado")
                print("Jogador confirmou")
            else:
                self.__gui.root.after(delay, self.__waitConf)
        else:
            past = time.perf_counter()
            if past - self.timer1 >= 10:
                self.__me.sendto(b'Get Game', (HOST,PORT))
                self.__gui.root.after(delay, self.connect)
            else:
                if ret == -1:
                    print("game reset in waitConf")
                    self.__resetGame()
                    self.__me.sendto(b'Get Game', (HOST, PORT))
                    self.__gui.root.after(delay, self.connect)
                else:
                    self.__gui.root.after(delay, self.__waitConf)
        return

    def __nbRecv(self):
        ready_to_read, ready_to_write, in_error = select.select([self.__me], [], [], 0)  # Checa se há pacotes no buff
        for sock in ready_to_read:  # se ready_to_read nao for uma lista vazia executa isso
            try:
                msg, addr = sock.recvfrom(1024)
                return (msg,addr)
            except:
                print("Jogador desconectou. debug: nbRecv")
                return -1
        return None

    def __gameFinished(self):   #Checa cada linha, coluna e diagonal se algum jogador venceu.
        # Retorna se o jogo não terminou, se houve algum vencedor (e qual o vencedor) ou se houve empate.
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
        if self.past - self.timer1 >= 2:      #Envia de 3 em 3 segundos uma comfirmação de que está conetado.
            self.__me.sendto(b'Connected', self.__Opon)
            self.timer1 = time.perf_counter() #E seta o timer inicial para o tempo atual.
        return

    def sendPlay(self, i, j):
        if self.__isMyTurn():
            if (self.__table[i][j] == -1):    #Se jogada for válida, envia ao oponente
                self.__myMove = (i,j)
                self.__me.sendto(
                    (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn)).encode(),
                    self.__Opon)    #Envia jogada ao oponente
                self.__turn += 1    #Incrementa turno
                self.__timeState = True
                self.__gui.buttons[i][j].configure(text=self.__icon)
                self.__table[self.__myMove[0]][self.__myMove[1]] = self.__choice   #Salva jogada na tabela
                return True
        return False

    def __opTurn(self) -> None:
        self.past = time.perf_counter()
        if ((self.past - self.timer1) >= 12): #Se tiver passado 12 segundos sem nenhuma comunicação, desconeta.
            print("Jogador desconectado!")
            quit()
        ret = self.__nbRecv()
        if type(ret) == type ((1,2)):
            msg, addr = ret
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
        elif ret == -1:
            print("Jogador desconectado. debug: host inalcançável.")
            quit()
        if ((self.past - self.timer2) >= 7):
            self.__resendMove()                # reenvia jogada caso tenha se passado 7 segundos sem resposta
            self.timer2 = time.perf_counter()  # atualiza timer2
        return

    def run(self):
        # Guarda em x o estado do jogo
        x = self.__gameFinished()
        if (self.__timeState):                                  # Se variável de estado estiver setada, reseta timers.
            #print("timestate")
            self.timer1 = self.timer2 = time.perf_counter()
            self.__timeState = False
        if not (x):                                            # Se jogo não estiver terminado, executa if.
            # Checa de quem é o turno, coloca a string adequada na Label info, e chama myTurn ou opTurn, dependendo do turno
            if self.__isMyTurn():
                self.__gui.info.configure(text="Sua vez.")
                self.__myTurn()
            else:
                self.__gui.info.configure(text="Aguarde oponente.")
                self.__opTurn()
        else:       # Jogo terminou
            self.past = time.perf_counter() # salva tempo atual.
            if self.past - self.timer1 >= 7:   # Se houver passado 7 segundos, fecha programa.
                print("Jogador desconectou. debug: gameFinished timer")
                return
            if x == 1:      # Se venceu, espera confirmação do cliente, reenviando ultima jogada caso não receba
                print("Voce Venceu")
                self.__gui.info.configure(text = "Voce Venceu")
                msg = self.__nbRecv()
                if type(msg) == type((1,2)):
                    if msg[0] == b'Lost':
                        print("Adversario confirmou derrota.")
                        return
                elif msg == None:
                    self.__resendMove()
                    self.__gui.root.after(delay2, self.run)
                elif msg == -1:
                    print("Adversario desconectou antes de confirmar derrota.")
                return
            elif x == 2:    # Jogador perdeu o jogo. Envia confirmação ao adversário.
                print("Voce Perdeu")
                self.__me.sendto(b'Lost', self.__Opon)
                self.__gui.info.configure(text = "Voce Perdeu")
                return
            else:           # Dois jogadores confirmam o empate. Caso não confirme, jogador reenvia jogada.
                print("Deu velha")
                self.__gui.info.configure(text = "Deu Velha")
                self.__me.sendto(b'Lost', self.__Opon)
                msg = self.__nbRecv()
                if type(msg) == type((1, 2)):
                    if msg[0] == b'Lost':
                        return
                self.__resendMove()
                self.__gui.root.after(delay2, self.run)
                return
        self.__gui.root.after(delay, self.run)
        return

    def __resetGame(self):
        self.__Opon = None
        self.__choice = -1
        self.__turn = 0
        self.__table = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.__myMove = (-1, -1)
        self.timer1 = 0
        self.timer2 = 0
        self.past = 0
        self.__timeState = True
        self.__icon = ""
        self.__opicon = ""
        return

    def __resendMove(self):
        self.past = time.perf_counter()
        if (self.__myMove != (-1, -1)):
            # Se não for primeiro turno, reenvia a jogada (assume que o adversário não recebeu sua jogada)
            print("reenviando")
            self.__me.sendto(
                (str(self.__myMove[0]) + "," + str(self.__myMove[1]) + "," + str(self.__turn - 1)).encode(),
                self.__Opon)