import sqlite3
import math
import time

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM navMenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return [dict(row) for row in res]
        except sqlite3.Error as e:
            print("Error reading from DB: ", e)
        return []

    def addFood(self, title, description, price, type):
        try:
            self.__cur.execute("SELECT COUNT(*) as count FROM food WHERE title LIKE ?", (title,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Food with this name already exists")
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO food (title, description, price, type) VALUES (?, ?, ?, ?)", (title, description, price, type))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding food to DB: ", e)
            return False

        return True

    def getFood(self):
        sql = '''SELECT * FROM food'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return [dict(row) for row in res]
        except sqlite3.Error as e:
            print("Error reading from DB: ", e)
        return []


    def getFoodByAlias(self, alias):
        try:
            self.__cur.execute("SELECT * FROM food WHERE id LIKE ?", (alias,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except sqlite3.Error as e:
            print("Error reading from DB: ", e)
        return None
    
