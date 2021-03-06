import tkinter as tk
import Player as pl

class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x400')
        # frame esquerda
        self.frameL = tk.Frame(self.root, width=70, height=260, bg='Grey')
        self.frameL.grid(row=1, column=0, sticky="WNSE")
        # frame direita
        self.frameR = tk.Frame(self.root, width=70, height=260, bg='Grey')
        self.frameR.grid(row=1, column=2, sticky="EWNS")
        # frame topo
        self.frameT = tk.Frame(self.root, width=400, height=70, bg='Blue')
        self.frameT.grid(row=0, column=0, columnspan=3, sticky="N")
        # frame fundo
        self.frameB = tk.Frame(self.root, width=400, height=70, bg='Red')
        self.frameB.grid(row=2, column=0, columnspan=3, sticky="S")
        # frame meio
        self.frameM = tk.Frame(self.root, width=260, height=260, bg='Blue', borderwidth=14)
        self.frameM.grid(row=1, column=1, sticky="NSEW", ipadx=2, ipady=5)
        self.buttons=[ [tk.Button(self.frameM, text = " ", command = lambda: self.butP(0,0), width = 6, height = 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(0,1), width = 6, height = 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(0,2), width = 6, height = 2)],
                   [tk.Button(self.frameM, text = " ", command = lambda: self.butP(1,0), width = 6, height = 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(1,1), width = 6, height= 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(1,2), width = 6, height= 2)],
                   [tk.Button(self.frameM, text = " ", command = lambda: self.butP(2,0), width = 6, height = 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(2,1), width = 6, height= 2),
                    tk.Button(self.frameM, text = " ", command = lambda: self.butP(2,2), width = 6, height= 2)]]
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].grid(in_ = self.frameM, row = i, column = j, padx = 12, pady = 12, sticky = "SW")
        self.info = tk.Label(self.frameB, text = "Conectando...", bg = "Red", width = 57)
        self.info.pack(side="top", anchor = "n")
        self.op = tk.Label(self.frameB, text = "Oponente: ", bg = "Red", height =4)
        self.op.pack(side = "top", anchor = "n")
        self.player = tk.Label(self.frameT, text = "Jogador 1", height = 4, width = 57, bg = "Green")
        self.player.pack()
        self.game = pl.Game(self)
        self.game.initSock()
        self.game.connect()
        self.root.mainloop()


    def butP (self, i, j):
        if self.game.sendPlay(i,j):
            self.info.configure(text="Aguarde oponente.")
        return

int = Interface()

