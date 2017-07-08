import tkinter as tk
import _thread
import thread
import socket



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
                con, addr = self.sock.accept()
            finally:
                print("Get connection from:", (addr))
                threadObj = thread.Thread(con,addr)
                _thread.start_new_thread(threadObj.thread_func, ())

class Server(object):
    def __init__(self):
        self.socket = Server_socket()
        # Debug
        print('Server created.')


    def main(self):
        self.socket.wait_message()
        

# ------------------ MAIN ------------------
servidor = Server()
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
