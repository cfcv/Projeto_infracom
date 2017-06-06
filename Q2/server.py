import tkinter as tk
import socket
import sqlite3

class DataBase(object):
	def __init__(self):
		self.conn = sqlite3.connect('users.db')
		self.cur = self.conn.cursor()
		self.cur.executescript('''
			DROP TABLE IF EXISTS Users;
			CREATE TABLE Users(
				id INTEGER PRIMARY KEY AUTOINCREMENT,				
				login UNIQUE,
				password VARCHAR(20)
			);''')

class Folder(object):
	def __init__(self, n):
		self.name = n
		self.files = list()
		self.children_folders = list()
		self.permissions = list()
		#Debug
		print('Folder:',self.name,'created.')

class Server(object):
	def __init__(self):
		self.root = Folder('root')
		self.DB = DataBase()
		#self.socket = Server_socket()
		#Debug
		print('Server created.')


		

#root = tk.Tk()
#root.title('Projeto Infracom(Server)')
#Os dois comando abaixo são usados para definir o tamanho da janela
#root.resizable(width=False, height=False)
#root.geometry('{}x{}'.format(700,500))
#root.configure(background='black')

#interface = Servidor(root)
#root.mainloop()

#------------------ MAIN ------------------
servidor = Server()
