import imp
from pypushdeer import PushDeer
from Abstraction.ObserverABC import ObserverABC
from Model.Enum import ConfigKey
from Instruction.Singlton import Singleton
import logging
from .Config import Config
from Instruction.TgBot import TgBot

@Singleton
class NewTgMsgObserver(ObserverABC):
    def __init__(self) -> None:
        pass
    def notify(self, data, *args, **kwargs):
        tgBot = TgBot()
        logging.info(f"Receiving new msg {data}, now sending it")
        bot = tgBot.get_bot()
        bot.send_message(chat_id="", text="Hello world")

