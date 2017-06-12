import database
import socket



class Thread:

    def __init__(self, con, addr):
        self.user = None
        self.DB = None
        self.conSock = con
        self.conAddr = addr

    # cmd num:
    # -1 -> close
    # 1 -> getuser(login, senha)
    # 2 -> create user(login, senha)
    # 3 -> getfile(path/name)
    # 4 -> pushfile(path/name, tamanho)
    # 5 -> listfiles(directory)
    def execute(self, c, data):
        lista = data.split('%')
        if (c == 1):
            # Debug
            print("Executando comando getuser")
            login, senha = (lista[1], lista[2])
            self.user = self.DB.getUser(login, senha)
            msg = b''
            if isinstance(self.user, user.User):
                msg = b'Usuario ' + self.user.login.encode() + b' logado.'
            else:
                msg = b'Usuario ou Senha incorretos.'
            self.conSock.send(msg)
        elif (c == 2):
            # Debug
            print("Executando comando createuser")
            cmd, login, senha = data.split('%')
            self.user = self.DB.newUser(login, senha)
            msg = b''
            if isinstance(self.user, user.User):
                msg = b'Usuario ' + self.user.login.encode() + b' criado/logado.'
            else:
                msg = b'Nome de usuario ja existente.'
            self.conSock.send(msg)
        elif (c == 3):
            print("Executando comando getfile")
        elif (c == 4):
            print("Executando comando pushfile")
            cmd, pathName, tam = data.split('%')
            file = b''
            while len(file) <= tam:
                file = file + self.conSock.recv(4096)
            # salva arquivo em login/path/nome


    def check_command(self, string):
        check = string.split('%')
        command = check[0]
        # Debug
        print("Commando ", command, " reconhecido")
        if (command == "getuser"):
            return 1
        elif (command == "createuser"):
            return 2
        elif (command == "getfile"):
            return 3
        elif (command == "pushfile"):
            return 4
        elif (command == "listfiles"):
            return 5
        elif (command == "close"):
            return -1
        else:
            return 0

    def thread_func(self):
        # Debug
        self.DB = database.DataBase()
        print("Thread criada para cliente:", self.conAddr)
        while True:
            data = self.conSock.recv(1024)
            if (len(data) < 1): continue
            data = data.decode()
            # Debug
            print("Mensagem recebida de", self.conAddr, ":", data)
            c = self.check_command(data)
            if (c == -1):
                print("Closing connection to", self.conAddr)
                client.close()
                break
            self.execute(c, data)