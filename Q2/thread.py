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
    # 2 -> createuser(login, senha)
    # 3 -> getfile("path/name")
    # 4 -> pushfile("path/name", tamanho)
    # 5 -> listfiles
    # 6 -> sharefile(usr, "directory/file")
    # 7 -> sharedir(usr, "directory")
    # 8 -> createdir("directory")
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
                msg = msg + b'\n' + self.__listShared()
                print(msg.decode())
                self.conSock.send(msg)
            else:
                print("Nao esta logado.")
                msg = b'Eh preciso logar'
                self.conSock.send(msg)
        elif (c == 6):
            print("Executando comando sharefile.")
            self.__sharefile(lista)
        elif (c == 7):
            print("Executando comando sharedir")
            usr, path = (lista[1], lista[2])
            if os.path.isdir("root/" + self.user.login + "/" + path):
                try:
                    if self.__sharedir(lista):
                        self.conSock.send(b'Diretorio compartilhado com sucesso')
                    else:
                        self.conSock.send(b'Usuario invalido.')
                except:
                    self.conSock.send(b'Houve um erro no compartilhamento do diretorio.')
            else:
                print(path + " -> is not a valid path")
                self.conSock.send(path.decode() + b' -> nao eh um caminho valido.')
        elif (c == 8):
            print("Executando comando createdir")
            pathName = lista[1] + "/"
            try:
                self.__createDir(pathName)
            except:
                self.conSock.send(b'Houve um erro na criacao do diretorio.')
                return
            self.conSock.send(b'Diretorio criado com sucesso.')


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
            fname = lista[1]
            file = None
            print("opening file: root/" + self.user.login + "/" + fname)
            try:
                file = open("root/"+self.user.login + "/" + fname, 'r')
            except:
                if self.DB.isShared(self.user.id, fname):
                    file = open("root/" + fname)
                else:
                    msg = b'Arquivo inexistente'
                    print(msg.decode() + ".")
                    self.conSock.send(msg)
                    return
            msg = file.read().encode()
            self.conSock.send(b'Ok%'+str(len(msg)).encode())
            self.conSock.send(msg)
        else:
            print("Nao esta logado.")
            msg = b'Eh preciso logar'
            self.conSock.send(msg)

    def __pushFile(self, lista):
        if self.user != None:
            try:
                # Separa pathName e tamanho do arquivo. Se for um caminho válido, abre um arquivo em modo escrita,
                # e recebe pacotes de 4096 bytes até completar o tamanho do arquivo. Confirma o recebimento enviando um OK
                pathName, tam = (lista[1], lista[2])
                if os.path.isabs("/root/" + self.user.login + "/" + pathName):
                    self.__createDir(pathName)
                    file = open("root/" + self.user.login + "/" + pathName, 'w+')
                    rcvlen = 0
                    tam = int(tam)
                    while rcvlen <= tam:
                        block = self.conSock.recv(4096)
                        rcvlen += 4096
                        file.write(block.decode())
                    self.conSock.send(b'Ok')
                else:
                    self.conSock.send(b'Path invalida.')
            except:
                print("Houve um erro no processo de salvar o arquivo.")
                self.conSock.send(b'Erro no procedimento. Tente novamente.')
        else:
            print("Nao esta logado.")
            msg = b'Eh preciso logar'
            self.conSock.send(msg)
        return

    def __createDir(self, pathName):
        os.makedirs("root/" + self.user.login + "/" + os.path.dirname(pathName), exist_ok=True)
        return

    def __listfiles(self, path) -> bytes:
        n = path.count("/") - 1
        print("n: ", n)
        flist, dlist = self.__scandir(path)
        msg = b""
        for file in flist:
            msg = msg + n * b"    " + file.encode() + b"\n"
        for dir in dlist:
            msg = msg + n*b"    " + b"[DIR] " + dir.encode() + b":\n" + self.__listfiles(path + "/" + dir)
        return msg

    def __listShared(self) -> bytes:
        ret = b'[ SHARED ]:\n'
        if self.user != None:
            shr = self.DB.getSharedFiles(self.user.id)
            if shr == None or len(shr) == 0:
                print("None wtf.!!!")
            for file in shr:
                file = file[0]
                print("file: ", file)
                ret = ret + b'  ' + file.encode() + b'\n'
        else:
            print("Nao esta logado.")
            msg = b'Eh preciso logar'
            self.conSock.send(msg)
        return ret

    def __sharefile(self, lista):
        usr, path = (lista[1], lista[2])
        path = self.user.login +"/"+path
        if os.path.isfile("root/"+path):
            if self.DB.newUsrFile(usr, path):
                self.conSock.send(b'Arquivo compartilhado com sucesso.')
            else:
                self.conSock.send(b'Usuario invalido.')
        else:
            print("is not file")
            self.conSock.send(b'Path is not a file.')

    def __sharedir(self, lista):
        ret = True
        usr, path = (lista[1], lista[2])
        flist, dlist = self.__scandir("root/"+ self.user.login + "/" + path)
        for file in flist:
            if not self.DB.newUsrFile(usr, self.user.login+ "/" + path+"/"+file):
                return False
        for dir in dlist:
           ret = ret and self.__sharedir([" ", usr, path+"/"+dir])
        return ret

    def __scandir(self, path):
        n = path.count("/") - 1
        scan = os.scandir(path)
        flist = [(x.name) for x in scan if x.is_file()]
        scan = os.scandir(path)
        dlist = [x.name for x in scan if x.is_dir()]
        return (flist, dlist)

    def check_command(self, string):
        check = string.split('%')
        command = check[0]
        # Debug
        #print("Commando ", command, " reconhecido")
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
        elif (command == "sharefile"):
            return 6
        elif (command == "sharedir"):
            return 7
        elif (command == "createdir"):
            return 8
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
                self.DB.closeDB()
                self.conSock.close()
                break
            self.execute(c, data)