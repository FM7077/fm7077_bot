from unicodedata import name
from Service.Config import Config as conf
from Service.NewTgMsgObserver import NewTgMsgObserver
from Service.NewTgMsgSubject import NewTgMsgSubject
from Instruction.TgBot import TgBot
from Service.TgBotService import TgBotService

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

if __name__ == "__main__":
    Initial()
    sub = NewTgMsgSubject()

    # polling in the end, to avoid thread 
    TgBot().get_updater().start_polling()
    TgBot().get_updater().idle()