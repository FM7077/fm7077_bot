from Model.PO import User, WeatherSub
from Service.UserService import UserService
from Service.WeatherSubService import WeatherSubService
from Service.CaiyunService import CaiyunService
from Instruction.Singleton import Singleton
from Model.DTO import Location, MsgToTG
from Instruction.TgBot import TgBot
import json
from Service.NewTgMsgSubject import NewTgMsgSubject

@Singleton
class WeatherReportService():
    def __init__(self) -> None:
        self.cy = CaiyunService()
        self.bot = TgBot().get_bot()
        self.tgMsgSub = NewTgMsgSubject()
        pass

    def run(self):
        subs = WeatherSubService().ListAll()
        wss = []
        for sub in subs:
            ws = WeatherSub(sub)
            wss.append(ws)
        for ws in wss:
            user = UserService().getUserByUserID(ws.UserID)
            userLang = user.Language
            if(user.IsInvalid()):
                continue
            loc = Location(ws.Longitude, ws.Latitude)
            result = self.cy.check_by_location(loc)
            resultMsg = self.cy.getReportMsg(result, userLang)
            self.processAlert(user, ws, result)
            self.processForecastKeypoing(user, ws, result)
    
    def processAlert(self, user: User, weatherSub: WeatherSub, result):
        newAlert = result["alert"]["content"]
        newAlertStr = json.dumps(newAlert)
        if(newAlertStr == weatherSub.LastAlert):
            return
        alertMsg = self.cy.getAlertMsg(result)
        weatherSub.LastAlert = newAlertStr
        WeatherSubService().UpsertByTgID(weatherSub)
        if(not alertMsg):
            return
        msgToTG = MsgToTG(user.TgChatID, alertMsg)
        self.tgMsgSub.data = msgToTG
        # self.bot.send_message(chat_id=user.TgChatID, text=alertMsg)
    
    def processForecastKeypoing(self, user: User, weatherSub: WeatherSub, result):
        fk = result["forecast_keypoint"]
        if(fk == weatherSub.LastForecastKeyPoint):
            return
        weatherSub.LastForecastKeyPoint = fk
        WeatherSubService().UpsertByTgID(weatherSub)
        msgToTG = MsgToTG(user.TgChatID, fk)
        self.tgMsgSub.data = msgToTG
        self.bot.send_message(chat_id=user.TgChatID, text=fk)