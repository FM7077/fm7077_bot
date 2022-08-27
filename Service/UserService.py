from sqlite_utils import Database
import sqlite3
from Model.PO import User
from Model.Enum import Setting, Language as langE
from Instruction.Singleton import Singleton

@Singleton
class UserService():
    def __init__(self) -> None:
        pass

    def upsertTgUser(self, user):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableUser.value]
        u = User()
        u.TgFirstName = user.first_name
        u.TgID = user.id
        u.TgChatID = user.chatid
        u.TgName = user.username
        u.Language = user.lang
        udict = u.__dict__
        userId = table.upsert(udict, hash_id_columns=("TgID",)).last_pk
        return userId
    
    def getTgUserLang(self, tgId: int = 0):
        existUser = self.getUserByTgID(tgId)
        if(None != existUser and None != existUser.Language):
            return langE[existUser.Language]
        else:
            return langE.ENG
    
    def getUserByTgID(self, tgID: int) -> User:
        db = Database(Setting.DBName.value)
        defaultUser = User()
        defaultUser.id = None
        existUser = next(db.query(
            f"select *from {Setting.DBTableUser.value} where TgID = :TgID",
            {"TgID": tgID}
        ), defaultUser.__dict__)
        return User(existUser)
    
    def getUserByUserID(self, userID) -> User:
        db = Database(Setting.DBName.value)
        defaultUser = User()
        defaultUser.id = None
        existUser = next(db.query(
            f"select *from {Setting.DBTableUser.value} where id = :id",
            {"id": userID}
        ), defaultUser.__dict__)
        return User(existUser)