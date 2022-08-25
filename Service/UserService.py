from sqlite_utils import Database
from Model.PO import User
from Model.Enum import Setting, Language as langE

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
        table.upsert(udict, pk="TgID")
    
    def getTgUserLang(self, tgId):
        db = Database(Setting.DBName.value)
        existUser = db.execute(f"select *from {Setting.DBTableUser.value} where TgID = '{tgId}'").fetchone()
        if(None != existUser and None != existUser[5]):
            return langE[existUser[5]]
        else:
            return langE.ENG