from flask_login import UserMixin
from flask import url_for, send_from_directory

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else "NoName"
    
    def getEmail(self):
        return self.__user['email'] if self.__user else "Without Email"
    
    def getPhone(self):
        return self.__user['phone'] if self.__user else "Without Phone"
    
    def getMoney(self):
        return self.__user['balance'] if self.__user else "Without Balance"