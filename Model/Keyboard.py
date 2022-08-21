from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Model.Language import ENG
from Model.Enum import TgCallBackType

class WRKeyboard():
    def __init__(self, param) -> None:
        minutely = InlineKeyboardButton(ENG.OPT_WR_MINUTELY.value, callback_data=f"{TgCallBackType.OPT_WR_MINUTELY.value}_{param}")
        hourly = InlineKeyboardButton(ENG.OPT_WR_HOURLY.value, callback_data=f"{TgCallBackType.OPT_WR_HOURLY.value}_{param}")
        daily = InlineKeyboardButton(ENG.OPT_WR_DAILY.value, callback_data=f"{TgCallBackType.OPT_WR_DAILY.value}_{param}")

        realtime = InlineKeyboardButton(ENG.OPT_WR_REALTIME.value, callback_data=f"{TgCallBackType.OPT_WR_REALTIME.value}_{param}")

        self.keyboard = [[minutely, hourly, daily], [realtime]]

    def get(self):
        return InlineKeyboardMarkup(self.keyboard)
