from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Model.Language import langE, LANG
from Model.Enum import TgCallBackType, LanguageList as ll
from Model.PO import WeatherSub, User
from Service.WeatherSubService import WeatherSubService
import math

class Keyboards():
    def __init__(self) -> None:
        pass
    def getWRKB(self, param, userLang):
        lang = LANG(userLang)
        minutely = InlineKeyboardButton(lang.l(ll.OPT_WR_MINUTELY), callback_data=f"{TgCallBackType.OPT_WR_MINUTELY.value}_{param}")
        hourly = InlineKeyboardButton(lang.l(ll.OPT_WR_HOURLY), callback_data=f"{TgCallBackType.OPT_WR_HOURLY.value}_{param}")
        daily = InlineKeyboardButton(lang.l(ll.OPT_WR_DAILY), callback_data=f"{TgCallBackType.OPT_WR_DAILY.value}_{param}")

        realtime = InlineKeyboardButton(lang.l(ll.OPT_WR_REALTIME), callback_data=f"{TgCallBackType.OPT_WR_REALTIME.value}_{param}")

        keyboard = [[minutely, hourly, daily], [realtime]]
        return InlineKeyboardMarkup(keyboard)

    def get24HKB(self): # 24 hours keyboard
        keyboard = [[0 for col in range (6)] for row in range (4)]
        i = 0
        for rowI, row in enumerate(keyboard):
            for colI, col in enumerate(row):
                showTxt = str(i).zfill(2)
                hi = InlineKeyboardButton(showTxt, callback_data=f"{TgCallBackType.SUB_WR_SETH.value}_{showTxt}")
                keyboard[rowI][colI] = hi
                i += 1
        return InlineKeyboardMarkup(keyboard)

    def getCMin(self): # step: 5 minutes keyboard
        keyboard = [[0 for col in range (6)] for row in range (2)]
        i = 0
        for rowI, row in enumerate(keyboard):
            for colI, col in enumerate(row):
                showTxt = str(i).zfill(2)
                hi = InlineKeyboardButton(showTxt, callback_data=f"{TgCallBackType.SUB_WR_SETM.value}_{showTxt}")
                keyboard[rowI][colI] = hi
                i += 5
        return InlineKeyboardMarkup(keyboard)

    def getSubWRKB(self, userLang): # sub weather report confirm
        lang = LANG(userLang)
        keyboard = [[InlineKeyboardButton(lang.l(ll.BTN_CANCEL), callback_data=f"{TgCallBackType.SUB_WR_CANCEL.value}")],
                        [InlineKeyboardButton(lang.l(ll.BTN_CONFIRM), callback_data=f"{TgCallBackType.SUB_WR_CONFIRM.value}")]]
        return InlineKeyboardMarkup(keyboard)

    def getSubsKB(self, user: User):
        subs = []
        for sub in WeatherSubService().listByUserID(user.id):
            ws = WeatherSub(sub)
            subs.append(ws)
        countSubs = len(subs)
        countRows = math.ceil(countSubs / 2)
        keyboard = [[] for row in range(countRows)]
        for ind, sub in enumerate(subs):
            keyboard[int(ind/2)].append(InlineKeyboardButton(sub.Name, callback_data=f"{TgCallBackType.SUB_WR_DETAIL.value}_{sub.id}"))
        return InlineKeyboardMarkup(keyboard)

    def getSubManKB(self, userLang: LANG, subid: str):
        lang = LANG(userLang)
        keyboard = [[InlineKeyboardButton(lang.l(ll.BTN_ED_SUB), callback_data=f"{TgCallBackType.SUB_WR_EDIT.value}_{subid}")
                        , InlineKeyboardButton(lang.l(ll.BTN_DEL_SUB), callback_data=f"{TgCallBackType.SUB_WR_DELETE.value}_{subid}")],
                        [InlineKeyboardButton(lang.l(ll.BTN_BACK_SUB_LIST), callback_data=f"{TgCallBackType.LIST_SUBS.value}")]]
        return InlineKeyboardMarkup(keyboard)
    
    def getDelSubKB(self, userLang: LANG, subid: str):
        lang = LANG(userLang)
        keyboard = [[InlineKeyboardButton(lang.l(ll.BTN_CANCEL), callback_data=f"{TgCallBackType.SUB_WR_DEL_CANCEL.value}_{subid}")],
                        [InlineKeyboardButton(lang.l(ll.BTN_DEL_SUB), callback_data=f"{TgCallBackType.SUB_WR_DEL_CONFIRM.value}_{subid}")]]
        return InlineKeyboardMarkup(keyboard)