import database
import user
import os

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
    # 3 -> getfile("path/name")
    # 4 -> pushfile("path/name", tamanho)
    # 5 -> listfiles("directory")
    # 6 -> share(usr, "directory/file")
    def execute(self, c, data):
        lista = data.split('%')
        if (c == 1):
            # Procura pelo usuario fornecido, e se senha estiver correta, loga.
            print("Executando comando getuser")
            self.__getUser(lista)
        elif (c == 2):
            # Cria novo usuario e loga no mesmo
            print("Executando comando createuser")
            self.__newUser(lista)
        elif (c == 3):
            # Se estiver logado, envia arquivo para cliente
            print("Executando comando getfile")
            self.__getFile(lista)
        elif (c == 4):
            # Se estiver logado, recebe arquivo do cliente
            print("Executando comando pushfile")
            self.__pushFile(lista)
        elif (c == 5):
            # Se estiver logado, envia ao cliente a arvore de diretorios/arquivos
            if self.user != None:
                msg = self.__listfiles("root/"+self.user.login)
                self.conSock.send(msg)
            else:
                print("Nao esta logado.")
                msg = b'Eh preciso logar'
                self.conSock.send(msg)

    def __getUser(self, lista):
        login, senha = (lista[1], lista[2])
        self.user = self.DB.getUser(login, senha)
        msg = b''
        if isinstance(self.user, user.User):
            msg = b'Usuario ' + self.user.login.encode() + b' logado'
        else:
            msg = b'Usuario ou Senha incorretos'
        self.conSock.send(msg)

    def __newUser(self, lista):
        login, senha = (lista[1], lista[2])
        self.user = self.DB.newUser(login, senha)
        if isinstance(self.user, user.User):
            msg = b'Usuario ' + self.user.login.encode() + b' criado/logado'
        else:
            msg = b'Nome de usuario ja existente'
        self.conSock.send(msg)

    def __getFile(self, lista):
        if self.user != None:
            self.conSock.send(b'Ok')
            fname = lista[1]
            print("root/" + self.user.login + "/" + fname)
            try:
                file = open("root/"+self.user.login + "/" + fname, 'r')
            except:
                msg = b'Arquivo inexistente'
                print(msg.decode() + ".")
                self.conSock.send(msg)
                return
            msg = file.read().encode()
            self.conSock.send(msg)
        else:
            print("Nao esta logado.")
            msg = b'Eh preciso logar'
            self.conSock.send(msg)

    def __pushFile(self, lista):
        if self.user != None:
            self.conSock.send(b'Ok')
            pathName, tam = (lista[1], lista[2])
            os.makedirs("root/" + self.user.login + "/" + os.path.dirname(pathName), exist_ok=True)
            file = open("root/" + self.user.login + "/" + pathName, 'w+')
            rcvlen = 0
            tam = int(tam)
            while rcvlen <= tam:
                block = self.conSock.recv(4096)
                rcvlen += 4096
                file.write(block.decode())
        else:
            print("Nao esta logado.")
            msg = b'Eh preciso logar'
            self.conSock.send(msg)

    def __listfiles(self, path) -> bytes:
        n = path.count("/")
        scan = os.scandir(path)
        flist = [(n * "    " + x.name + "\n") for x in scan if x.is_file()]
        scan = os.scandir(path)
        dlist = [x.name for x in scan if x.is_dir()]
        msg = b""
        for file in flist:
            msg = msg + file.encode()
        for dir in dlist:
            msg = msg + n*b"    " + b"[DIR] " + dir.encode() + b":\n" + self.__listfiles(path + "/" + dir)
        return msg


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
            try:
                data = self.conSock.recv(1024)
            except:
                if self.user is not None:
                    print("Closing thread for user " + self.user.login)
                else:
                    print("Closing thread without user")
                self.DB.closeDB()
                self.conSock.close()
                return None
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