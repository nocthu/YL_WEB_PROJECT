import sqlalchemy
import sqlite3
import datetime


class DataBase:
    def __init__(self):
        conn = sqlite3.connect("db/base.sqlite", check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class DataBaseUser(DataBase):
    def __init__(self):
        super().__init__()
        self.connection = self.get_connection()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class Advices:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS advises 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(100),
                             content VARCHAR(1000),
                             ingrid VARCHAR(100),
                             photo VARCHAR(100),
                             hard INTEGER,
                             date,
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, content, ingrid, photo, hard, user_id):
        cursor = self.connection.cursor()
        date = int(str(datetime.date.today()).split('-')[0]) * 364 + int(
            str(datetime.date.today()).split('-')[1]) * 30 + int(
            str(datetime.date.today()).split('-')[2])
        cursor.execute('''INSERT INTO advices 
                          (name, content, ingrid, photo,hard,date, user_id) 
                          VALUES (?,?,?,?,?,?,?)''', (name, content, ingrid, photo, hard, date, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, advices_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM advices WHERE id = ?", (str(advices_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM advices ORDER BY name ASC")
        rows = cursor.fetchall()
        return rows

    def delete(self, advices_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM advices WHERE id = ?''', (str(advices_id)))

        cursor.close()
        self.connection.commit()


