from tokenize import Double
from unicodedata import name
from Service.ConfigService import Config as conf
from Service.NewTgMsgObserver import NewTgMsgObserver
from Service.NewTgMsgSubject import NewTgMsgSubject
from Instruction.TgBot import TgBot
from Service.TgBotService import TgBotService
from sqlite_utils import Database
from Model.Enum import Language, Setting

def Initial():
    # init config
    conf()
    # init tg bot
    TgBot()
    TgBotService()
    
    # regist observer
    newTgMsgObs= NewTgMsgObserver()
    newTgMsgSub = NewTgMsgSubject()
    newTgMsgSub.add(newTgMsgObs)

    # init db
    db = Database(Setting.DBName.value)
    db[Setting.DBTableUser.value].create({
        "id": str,
        "TgID": int,
        "TgChatID": int,
        "TgName": str,
        "TgFirstName": str,
        "Language": str
    }, pk=("id"), if_not_exists=True)
    db[Setting.DBTableWeatherSub.value].create({
        "id": str,
        "UserID": str,
        "Name": str,
        "IsSub": bool,
        "IsSubAlert": bool,
        "Longitude": float,
        "Latitude": float,
        "ReportTime": str,
        "LastAlert": str,
        "LastForecastKeyPoint": str,
    }, pk="id", if_not_exists=True)

if __name__ == "__main__":
    Initial()
    sub = NewTgMsgSubject()

    # polling in the end, to avoid thread 
    TgBot().get_updater().start_polling()
    TgBot().get_updater().idle()