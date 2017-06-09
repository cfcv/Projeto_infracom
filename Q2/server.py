import tkinter as tk
import socket
import sqlite3
import os
import re
import _thread

def execute(c, client, data):
    lista = data.split('%')
    if(c == 1):
        #Debug
        print("Executando comando getuser")

    elif(c == 2):
        #Debug
        print("Executando comando createuser")


def check_command(string):
    check = string.split('%')
    command = check[0]
    #Debug
    print("Commando ",command,"reconhecido")
    if(command == "getuser"):
        return 1
    elif(command == "createuser"):
        return 2
    else:
        return 0


def thread_func(client,addr):
    #Debug
    print("Thread criada para cliente:", addr)
    while True:
        data = client.recv(1024)
        if (len(data) < 1): continue
        data = data.decode()
        #Debug
        print("Mensagem recebida de",addr,":",data)
        c = check_command(data)
        if(c == -1):
            print("Closing connection to", addr)
            client.close()
            break
        execute(c, client, data)

class Server_socket(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = "127.0.0.1"
        self.port = 35298
        self.sock.bind((self.ip, self.port))
        self.sock.listen(10)

    def wait_message(self):
        # Debug
        print("Waiting for connection.")
        while True:
            try:
                con, client = self.sock.accept()
            finally:
                print("Get connection from:", (client))
                _thread.start_new_thread(thread_func, (con,client))

class DataBase(object):
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,               
                login VARCHAR(20) UNIQUE,
                password VARCHAR(20)
            );
            
            CREATE TABLE IF NOT EXISTS Dirs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS UsrDirs(
                usrID INTEGER,
                dirID INTEGER,
                constraint UsrDir_pk PRIMARY KEY (usrID,dirID),
                constraint usr_fk FOREIGN KEY (usrID) REFERENCES Users,
                constraint dir_fk FOREIGN KEY (dirID) REFERENCES Dirs
            );""")

    def newFolder(self, login, folderName):
        self.cur.execute("""
        INSERT INTO Dirs(path) VALUES (?)""", login+"/"+folderName)
        self.conn.commit()

    def newUser(self, login, password):
        self.cur.execute("""
        INSERT INTO Users(login, password) VALUES (?,?)""", (login, password))
        self.cur.execute("""
        INSERT INTO Dirs(path) VALUES (?)""", login)
        self.conn.commit()

    def newUsrDir(self, usrID, dirID):
        self.cur.execute("""
        INSERTO INTO UsrDirs(usrID, dirID) VALUES (?,?)""", (usrID, dirID))
        self.conn.commit()

    def check_user(self, usuario, senha):
        self.cur.execute("""SELECT login, password FROM Users WHERE login=(?) AND password=(?)""", (usuario,senha))
        self.result = self.cur.fetchone()
        if(self.result is None):
            return False
        else:
            return True


class Server(object):
    def __init__(self):
        self.DB = DataBase()
        self.socket = Server_socket()
        # Debug
        print('Server created.')


    def main(self):
        self.socket.wait_message()
        

# ------------------ MAIN ------------------
servidor = Server()
#servidor.addFolder("root")
servidor.main()





#Comanetários
# class RegularExpression(object):
#     def procura(self, fname, name):
#         self.file = open(fname, 'r')
#         for line in self.file:
#             if (not line.startswith('d')): continue
#             self.palavras = line.split()
#             self.foldername = self.palavras[8]
#             if (self.foldername == name):
#                 return True
#         return False
    #Atributos da classe SERVEr
        #self.regular = RegularExpression()
        #self.out = "output.txt"
    #funções da classe server
    # def addFolder(self, name):
    #     os.system("ls -l > " + self.out)
    #     if (self.regular.procura(self.out, name)):
    #         print("Sorry this folder already exists(" + name + ")")
    #     else:
    #         pass
    #         os.system("mkdir"+name)
    #         self.DB.newFolder(user.path+"/"+name)

    # def execute(self, com):
    #     if (com[0] == "getuser"):
    #         # Debug
    #         print("comando getuser reconhecido")
    #         # self.DB.get_user()
#Interface
# root = tk.Tk()
# root.title('Projeto Infracom(Server)')
# Os dois comando abaixo são usados para definir o tamanho da janela
# root.resizable(width=False, height=False)
# root.geometry('{}x{}'.format(700,500))
# root.configure(background='black')

# interface = Servidor(root)
# root.mainloop()
