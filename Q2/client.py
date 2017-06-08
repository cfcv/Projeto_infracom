import tkinter as tk
import socket


class Conexao(object):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ip = '127.0.0.1'
		self.port = 35298
		#Debug
		print("Client socket created.")
		self.sock.connect((self.ip,self.port))
		print("Connected")
		
	def send(self,mss):
		#Debug
		print("Enviando mensagem:",mss)
		self.sock.send(mss.encode())

class GUI_User(object):
	def __init__(self,master): #,conection, address):
		#self.conn = conection
		#self.addr = address
		
		#---- Frames ----
		self.frame1 = tk.Frame(master)
		self.frame2 = tk.Frame(master)
		self.frame3 = tk.Frame(master)
		self.frame4 = tk.Frame(master)
		self.frame5 = tk.Frame(master)
		
		#---- Labels ----
		self.titulo = tk.Label(self.frame1,text='Remote File Directory', bg='black', fg='red', font=("times",32,"bold italic"), height=5)		
		self.username = tk.Label(self.frame2,text='Username:', bg='black', fg='green', font=("times",12,"bold"), padx=50)
		self.senha = tk.Label(self.frame2, text='Password:', bg='black', fg='green', font=("times",12,"bold"), padx=51)
		self.espaco1 = tk.Label(self.frame2, bg='black', padx=87, pady=15)
		self.espaco2 = tk.Label(self.frame2, bg='black', padx=93, pady=15)
		self.espaco3 = tk.Label(self.frame5, bg='black', padx=35, pady=5)		
		self.repeat = tk.Label(self.frame4, text='Repeat password:', bg='black', font=("times",12,"bold"), fg='green', padx=26)

		#---- Entrys ----
		self.user = tk.Entry(self.frame2, width=22, bd=4, bg='green', fg='black', highlightcolor='red')
		self.senhaEntry = tk.Entry(self.frame2, width=22, bd=4, bg='green', fg='black', highlightcolor='red')
		self.repeatEntry = tk.Entry(self.frame4, width=22, bd=4, bg='green', fg='black', highlightcolor='red')
		
		#---- Buttons ----
		self.submit = tk.Button(self.frame3, text='Log in', background='green', command=self.enviar, borderwidth=4, width=10, cursor='dot')
		self.createAccount = tk.Button(self.frame3, text='Create an account', background='red', command=self.criar_conta, borderwidth=4, cursor='cross')
		self.create = tk.Button(self.frame5, text='Create', background='red', width=5, borderwidth=3, command=self.create_buttom)

		#Debu3
		print("Client is running")
		#socket
		self.conn = Conexao()

	def enviar(self):
		self.userText = self.user.get()
		self.senhaText = self.senhaEntry.get()
		
		if (len(self.userText) < 1) or (len(self.senhaText) < 1):
			print("No data")
		else:
			self.message = "getuser%"+self.userText+"%"+self.senhaText
			self.conn.send(self.message)

	def inicializar(self):
		self.frame1.pack()
		self.frame2.pack()
		self.frame3.pack()
		self.titulo.pack()
		self.username.grid(row=0, column=0)
		self.user.grid(row=0, column=1)
		self.senha.grid(row=1,column=0)
		self.senhaEntry.grid(row=1, column=1)
		self.espaco1.grid(row=2, column=0)
		self.espaco2.grid(row=2,column=1)
		self.submit.pack(side = 'right')
		self.createAccount.pack(side = 'left')

	def criar_conta(self):
		self.frame3.pack_forget()
		self.frame4.pack()
		self.repeat.pack(side='left')
		self.repeatEntry.pack(side='right')
		self.frame5.pack()
		self.espaco3.pack()
		self.create.pack()

	def create_buttom(self):
		self.userText = self.user.get()
		self.senhaText = self.senhaEntry.get()
		self.repeatText = self.repeatEntry.get()
		print(self.userText,self.senhaText,self.repeatText)


#-------------------------- MAIN -------------------------- 		
root = tk.Tk()
root.title('Sistema de arquivos')


root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(700,500))
root.configure(background='black')
interface = GUI_User(root)
interface.inicializar()
root.mainloop()
