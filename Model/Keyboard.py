from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Model.Language import langE, LANG
from Model.Enum import TgCallBackType, LanguageList as ll

class WRKeyboard():
    def __init__(self, param, userLang) -> None:
        lang = LANG(userLang)
        minutely = InlineKeyboardButton(lang.l(ll.OPT_WR_MINUTELY), callback_data=f"{TgCallBackType.OPT_WR_MINUTELY.value}_{param}")
        hourly = InlineKeyboardButton(lang.l(ll.OPT_WR_HOURLY), callback_data=f"{TgCallBackType.OPT_WR_HOURLY.value}_{param}")
        daily = InlineKeyboardButton(lang.l(ll.OPT_WR_DAILY), callback_data=f"{TgCallBackType.OPT_WR_DAILY.value}_{param}")

        realtime = InlineKeyboardButton(lang.l(ll.OPT_WR_REALTIME), callback_data=f"{TgCallBackType.OPT_WR_REALTIME.value}_{param}")

        self.keyboard = [[minutely, hourly, daily], [realtime]]

    def get(self):
        return InlineKeyboardMarkup(self.keyboard)

class Keyboard_Hour(): # 24 hours keyboard
    def __init__(self) -> None:
        self.keyboard = [[0 for col in range (6)] for row in range (2)]
        i = 1
        for rowI, row in enumerate(self.keyboard):
            for colI, col in enumerate(row):
                hi = InlineKeyboardButton(i, callback_data=f"{TgCallBackType.SUB_WR_SETH.value}_{i}")
                self.keyboard[rowI][colI] = hi
                i += 1
    def get(self):
        return InlineKeyboardMarkup(self.keyboard)

class Keyboard_CMin(): # step: 5 minutes keyboard
    def __init__(self) -> None:
        self.keyboard = [[0 for col in range (6)] for row in range (2)]
        i = 0
        for rowI, row in enumerate(self.keyboard):
            for colI, col in enumerate(row):
                hi = InlineKeyboardButton(i, callback_data=f"{TgCallBackType.SUB_WR_SETM.value}_{i}")
                self.keyboard[rowI][colI] = hi
                i += 5
    def get(self):
        return InlineKeyboardMarkup(self.keyboard)

class Keyboard_SubWR_Confirm():
    def __init__(self, userLang) -> None:
        lang = LANG(userLang)
        self.keyboard = [[InlineKeyboardButton(lang.l(ll.BUT_CANCEL), callback_data=f"{TgCallBackType.SUB_WR_CANCEL.value}")],
                        [InlineKeyboardButton(lang.l(ll.BUT_CONFIRM), callback_data=f"{TgCallBackType.SUB_WR_CONFIRM.value}")]]
    def get(self):
        return InlineKeyboardMarkup(self.keyboard)