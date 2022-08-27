import imp
from pypushdeer import PushDeer
from Abstraction.ObserverABC import ObserverABC
from Model.DTO import MsgToTG
from Model.Enum import ConfigKey
from Instruction.Singleton import Singleton
import logging
from .ConfigService import Config
from Instruction.TgBot import TgBot

@Singleton
class NewTgMsgObserver(ObserverABC):
    def __init__(self) -> None:
        self.bot = TgBot().get_bot()
        pass
    def notify(self, data: MsgToTG, *args, **kwargs):
        logging.info(f"Receiving new msg {data}, now sending it")
        self.bot.send_message(chat_id=data.chatId, text=data.msg)

