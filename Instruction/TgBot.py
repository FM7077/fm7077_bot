from .Singlton import Singleton
from Service.Config import Config as conf
from Model.Enum import ConfigKey
from telegram.ext import (Updater)

@Singleton
class TgBot():
    def __init__(self) -> None:
        c = conf()
        tgbot_token = c.getByKey(ConfigKey.Tokens.value, ConfigKey.Tg_Bot.value)
        self.updater = Updater(token=tgbot_token, use_context=True)
    def get_updater(self):
        return self.updater
    def get_dispatcher(self):
        return self.updater.dispatcher
    def get_bot(self):
        return self.updater.bot