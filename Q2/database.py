import user
import sqlite3

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
        INSERT INTO Dirs(path) VALUES (?)""", login + "/" + folderName)
        self.conn.commit()

    def newUser(self, login, password):
        if (not self.check_user(login, password)):
            self.cur.execute("""
            INSERT INTO Users(login, password) VALUES (?,?)""", (login, password))
            self.cur.execute("""
            INSERT INTO Dirs(path) VALUES (?)""", (login,))
            self.conn.commit()
            return self.getUser(login, password)

    def newUsrDir(self, usrID, dirID):
        self.cur.execute("""
        INSERTO INTO UsrDirs(usrID, dirID) VALUES (?,?)""", (usrID, dirID))
        self.conn.commit()

    def check_user(self, usuario, senha):
        self.cur.execute("""SELECT login, password FROM Users WHERE login=(?) AND password=(?)""", (usuario, senha))
        result = self.cur.fetchone()
        if (result is None):
            return False
        else:
            return True

    def getUser(self, usuario, senha):
        self.cur.execute("""SELECT login, password, id FROM Users WHERE login=(?) AND password=(?)""", (usuario, senha))
        result = self.cur.fetchone()
        if (result is None):
            print("Usuario ou Senha invalidos.")
            # enviar mensagem ao usuário.
            return result
        else:
            login, passw, id = result
            usr = user.User(login, passw, id)
            return usr