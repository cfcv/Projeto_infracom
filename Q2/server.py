import tkinter as tk
import socket
import sqlite3
import os
import re


class RegularExpression(object):
	def procura(self, fname, name):
		self.file = open(fname,'r')
		for line in self.file:
			if(not line.startswith('d')): continue
			self.palavras = line.split()
			self.foldername = self.palavras[8]			
			if(self.foldername == name):
				return True
		return False


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
	


class Server(object):
	def __init__(self):
		#self.root = Folder('root')
		self.DB = DataBase()
		self.regular = RegularExpression()
		self.out = "output.txt"
		#self.socket = Server_socket()
		#Debug
		print('Server created.')


	def addFolder(self, name):
		os.system("ls -l > "+self.out)
		if(self.regular.procura(self.out, name)):
			print("Sorry this folder already exists("+name+")")
		else:
			pass			
			#os.system("mkdir"+name)		
			#self.DB.insert(user.path+"/"+name)

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
servidor.addFolder("root")
