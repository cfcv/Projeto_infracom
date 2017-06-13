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
    # 3 -> getfile("path/name")
    # 4 -> pushfile("path/name", tamanho)
    # 5 -> listfiles("directory")
    def execute(self, c, data):
        lista = data.split('%')
        if (c == 1):
            # Procura pelo usuario fornecido, e se senha estiver correta, loga.
            print("Executando comando getuser")
            login, senha = (lista[1], lista[2])
            self.user = self.DB.getUser(login, senha)
            msg = b''
            if isinstance(self.user, user.User):
                msg = b'Usuario ' + self.user.login.encode() + b' logado'
            else:
                msg = b'Usuario ou Senha incorretos'
            self.conSock.send(msg)
        elif (c == 2):
            # Cria novo usuario e loga no mesmo
            print("Executando comando createuser")
            cmd, login, senha = data.split('%')
            self.user = self.DB.newUser(login, senha)
            if isinstance(self.user, user.User):
                msg = b'Usuario ' + self.user.login.encode() + b' criado/logado'
            else:
                msg = b'Nome de usuario ja existente'
            self.conSock.send(msg)
        elif (c == 3):
            # Se estiver logado, envia arquivo para cliente
            if self.user != None:
                print("Executando comando getfile")
                self.conSock.send(b'Ok')
                cmd, fname = data.split("%")
                try:
                    file = open(self.user.login+"/"+fname.encode(), 'r')
                except:
                    msg = b'Arquivo inexistente'
                    print(msg.decode()+".")
                    self.conSock.send(msg)
                    return
                i = 0
                while i < len(file):
                    msg = file.read(4096)
                    self.conSock.send(msg)
                    i += 4096
            else:
                print("Nao esta logado.")
                msg = b'Eh preciso logar'
                self.conSock.send(msg)
        elif (c == 4):
            # Se estiver logado, recebe arquivo do cliente
            if self.user != None:
                print("Executando comando pushfile")
                self.conSock.send(b'Ok')
                cmd, pathName, tam = data.split('%')
                file = open(self.user.login+"/"+pathName, 'w')
                while len(file) <= tam:
                    block = self.conSock.recv(4096)
                    file.write(block.decode())
            else:
                print("Nao esta logado.")
                msg = b'Eh preciso logar'
                self.conSock.send(msg)
        elif (c == 5):
            # Se estiver logado, envia ao cliente a arvore de diretorios/arquivos
            if self.user != None:
                self.conSock.send(b'Ok')
                msg = self.__listfiles(self.user.login)
                self.conSock.send(msg)
            else:
                print("Nao esta logado.")
                msg = b'Eh preciso logar'
                self.conSock.send(msg)

    def __listfiles(self, path):
        n = path.count("/")
        scan = os.scandir(path)
        flist = [(n * "    " + x.name + "\n") for x in scan if x.is_file()]
        scan = os.scandir(path)
        dlist = [x.name for x in scan if x.is_dir()]
        msg = b""
        for file in flist:
            msg = msg + file.encode()
        for dir in dlist:
            msg = msg + n*b"    "+ b"[DIR] " + dir + b":\n" + self.__listfiles(path + "/" + dir)
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