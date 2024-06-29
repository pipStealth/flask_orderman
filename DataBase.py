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
    
    def addAccount(self, fullname, email, password, phone):
        try:
            self.__cur.execute("SELECT COUNT(*) as count FROM account WHERE email LIKE ?", (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Account with this email already exists")
                return False
            
            self.__cur.execute("INSERT INTO account (name, email, password, phone, offer, balance) VALUES (?, ?, ?, ?, ?, ?)", (fullname, email, password, phone, "None", 0))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding account to DB: ", e)
            return False

        return True
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM account WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            return res
        except sqlite3.Error as e:
            print("Error getting data from DB: "+str(e))

    def getUserByEmail(self, email):
        try:
            self.__cur.execute("SELECT * FROM account WHERE email = ?", (email,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except sqlite3.Error as e:
            print("Error reading user from DB: ", e)
        return None  # Измените False на None

    def getOrdersByUserId(self, user_id):
        try:
            self.__cur.execute("SELECT offer FROM account WHERE id = ?", (user_id,))
            res = self.__cur.fetchone()
            if res:
                offer_ids = res['offer'].split()  # Разделяем строку с ID заказов
                food_items = []
                for offer_id in offer_ids:
                    self.__cur.execute("SELECT * FROM food WHERE id = ?", (offer_id,))
                    food = self.__cur.fetchone()
                    if food:
                        food_items.append(dict(food))
                return food_items
        except sqlite3.Error as e:
            print("Error reading orders from DB: ", e)
        return []
    
    def userOrder(self, user_id, order_id):
        try:
            self.__cur.execute(f"SELECT * FROM account WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False

            current_offer = res["offer"]
            updated_offer = f"{current_offer} {order_id}" if current_offer != "None" else str(order_id)

            self.__cur.execute("UPDATE account SET offer = ? WHERE id = ?", (updated_offer, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error updating data in DB: "+str(e))
            return False
        return True

