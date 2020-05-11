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
                             email VARCHAR(50),
                             user_name VARCHAR(50),
                             password VARCHAR(128),
                             sex VARCHAR(50),
                             weight VARCHAR(50),
                             water VARCHAR(50),
                             status VARCHAR(50),
                             date VARCHAR(50),
                             percent VARCHAR(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, email, user_name, password_hash, sex, weight, status):
        cursor = self.connection.cursor()
        if sex == 'Ж':
            sex = (31, 'Ж')
        else:
            sex = (35, 'М')
        cursor.execute('''INSERT INTO users 
                          (email, user_name, password, sex, weight, water, status, date, percent) 
                          VALUES (?,?,?,?,?,?,?,?,?)''',
                       (email, user_name, password_hash, sex[1], weight, int(weight) * sex[0], status,
                        datetime.date.today(), 0))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def update(self, user_id, what, value):
        cursor = self.connection.cursor()
        if what == 'percent':
            cursor.execute("""UPDATE users
                            SET percent = ?
                            WHERE id = ?""", (value, str(user_id)))
        if what == 'date':
            cursor.execute("""UPDATE users
                            SET date = ?
                            WHERE id = ?""", (value, str(user_id)))
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, email, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?",
                       (email, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class Advices(DataBase):
    def __init__(self):
        super().__init__()
        self.connection = self.get_connection()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS advices 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(100),
                             content VARCHAR(1000),
                             photo VARCHAR(100),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, content, photo, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO advices 
                          (name, content, photo, user_id) 
                          VALUES (?,?,?,?)''', (name, content, photo, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, advices_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM advices WHERE id = ?", (str(advices_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM advices")
        rows = cursor.fetchall()
        return rows

    def delete(self, advices_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM advices WHERE id = ?''', (str(advices_id),))

        cursor.close()
        self.connection.commit()


class Cities(DataBase):
    def __init__(self):
        super().__init__()
        self.connection = self.get_connection()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cities 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             city_name VARCHAR(100),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, city_name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO cities 
                          (city_name) 
                          VALUES (?)''', (city_name,))
        cursor.close()
        self.connection.commit()

    def get(self, cities_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cities WHERE id = ?", (str(cities_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cities")
        rows = cursor.fetchall()
        return rows

    def delete(self, city_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM cities WHERE id = ?''', (str(city_id),))

        cursor.close()
        self.connection.commit()
