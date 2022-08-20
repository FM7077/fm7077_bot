from unicodedata import name
from Service.Config import Config as conf
from Service.NewTgMsgObserver import NewTgMsgObserver
from Service.NewTgMsgSubject import NewTgMsgSubject
from Instruction.TgBot import TgBot
from Service.TgBotService import TgBotService

def SetConfig():
    c = conf()
    tgBot = TgBot()
    tgBotService = TgBotService()
    newDeerMsgObs= NewTgMsgObserver()
    newDeerMsgSub = NewTgMsgSubject()
    newDeerMsgSub.add(newDeerMsgObs)

if __name__ == "__main__":
    SetConfig()
    sub = NewTgMsgSubject()

    # polling in the end, to avoid thread 
    TgBot().get_updater().start_polling()
    TgBot().get_updater().idle()