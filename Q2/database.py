import user
import os
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
                path VARCHAR(100) UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS UsrFile(
                usrID INTEGER,
                fpath VARCHAR2(100),
                constraint UsrFile_pk PRIMARY KEY (usrID,fpath),
                constraint usr_fk FOREIGN KEY (usrID) REFERENCES Users
            );""")

    def newFolder(self, login, folderName):
        """ Adiciona folder no banco de dados e no sistema de arquivos em root/login/newFolder """
        self.cur.execute("""
        INSERT INTO Dirs(path) VALUES (?)""", (login + "\\" + folderName,))
        os.makedirs("./root/"+login+"/"+folderName)
        self.conn.commit()

    def newUser(self, login, password):
        """ Adiciona novo usuário com login e senha caso não exista usuário com nome igual.
            Adiciona novo diretório no banco de dados"""
        if (not self.userExists(login)):
            self.cur.execute("""
            INSERT INTO Users(login, password) VALUES (?,?)""", (login, password))
            self.cur.execute("""
            INSERT INTO Dirs(path) VALUES (?)""", (login,))
            self.conn.commit()
            self.newFolder(login, "")
            return self.getUser(login, password)
        return None

    def newUsrFile(self, usr, fpath):
        if (self.userExists(usr)):
            self.cur.execute("""SELECT id FROM Users WHERE login=(?)""", (usr,))
            usrID = self.cur.fetchone()[0]
            self.cur.execute("""INSERT INTO UsrFile(usrID, fpath) VALUES (?,?)""", (usrID, fpath))
            self.conn.commit()
            return True
        else:
            print("User " + usr + " does not exist.")
            return False

    def getSharedFiles(self, id):
        self.cur.execute("""SELECT fpath FROM UsrFile WHERE usrID=(?)""", (id,))
        ret = self.cur.fetchall()
        return ret

    def isShared(self, id, fpath) -> bool:
        self.cur.execute("""SELECT usrID FROM UsrFile WHERE usrID=(?) AND fpath=(?)""", (id, fpath))
        ret = self.cur.fetchone()
        if ret == None:
            return False
        else:
            return True

    def check_user(self, usuario, senha) -> bool:
        self.cur.execute("""SELECT id FROM Users WHERE login=(?) AND password=(?)""", (usuario, senha))
        result = self.cur.fetchone()
        if (result is None):
            return False
        else:
            return True

    def userExists(self, usuario) -> bool:
        self.cur.execute("""SELECT id FROM Users WHERE login=(?)""", (usuario,))
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
            return result
        else:
            login, passw, id = result
            usr = user.User(login, passw, id)
            return usr

    def closeDB(self):
        self.cur.close()
        self.conn.close()
        print("DB fechado")
        return