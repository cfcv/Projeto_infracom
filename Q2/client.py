import socket

def evalCommand(c, sock):
	if c == 1:
		path = input("Digite o caminho do arquivo: ")
		spath = input("Digite o caminho onde o arquivo sera salvo: ")
		sock.send(b'getfile%' + path.encode())
		data = sock.recv(1024)
		if data.split(b'%')[0] == b'Ok':
			tam = int(data.split(b'%')[1])
			i = 0
			data = b''
			file = open(spath, 'w')
			while i < tam:
				data = sock.recv(4096)
				file.write(data.decode())
				i += 4096
			print("Arquivo:\n" + data.decode())
		else:
			print(data.decode())
	elif c == 2:
		dpath = input("Digite o caminho onde o arquivo sera salvo: ")
		path = input("Digite o caminho do arquivo a ser enviado: ")
		file = open(path, 'r')
		aux = file.read()
		sock.send(b'pushfile%'+dpath.encode()+b'%'+str(len(aux)).encode())
		sock.send(aux.encode())
	elif c == 3:
		path = input("Digite caminho do diretorio: ")
		sock.send(b'createdir%'+path)
		feedback = sock.recv(1024)
		print(feedback.decode())
	elif c == 4:
		usr = input("Digite usuario que voce quer compartilhar: ")
		path = input("Digite o caminho do arquivo a ser compartilhado: ")
		sock.send(b'sharefile%'+usr.encode()+b'%'+path.encode())
		feedback = sock.recv(1024)
		print(feedback.decode())
	elif c == 5:
		usr = input("Digite usuario que voce quer compartilhar: ")
		path = input("Digite o caminho do diretorio a ser compartilhado: ")
		sock.send(b'sharedir%' + usr.encode() + b'%' + path.encode())
		feedback = sock.recv(1024)
		print(feedback.decode())
	elif c == 6:
		sock.send(b'listfiles')
		tree = sock.recv(4096)
		print("Arvore de arquivos:\n"+tree.decode())
	elif c == 7:
		login = input("Digite seu login: ")
		senha = input("Digite sua senha: ")
		sock.send(b'getuser%'+login.encode()+b'%'+senha.encode())
		feedback = sock.recv(1024)
		print(feedback.decode())
	elif c == 8:
		login = input("Digite seu login: ")
		senha = input("Digite sua senha: ")
		sock.send(b'createuser%' + login.encode() + b'%' + senha.encode())
		feedback = sock.recv(1024)
		print(feedback.decode())
	elif c == 9:
		sock.send(b'close')
		quit()
	return

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 35298
sock.connect((ip,port))
print("Connected")
while True:
	print("Menu:\n[1] -> download file from server\n[2] -> upload file to server\n[3] -> create directory\n" +
		  "[4] -> share file with a specified user\n[5] -> share directory with a specified user\n" +
		  "[6] -> list your directory tree\n[7] -> login on an existing account\n[8] -> create a new account\n" +
		  "[9] -> quit\n")
	try:
		command = int(input("escolha: "))
		evalCommand(command, sock)
	except:
		print("Digite apenas um numero")
		continue
