from Model.Enum import Setting
from Model.PO import User, WeatherSub
from Service.UserService import UserService
from Service.WeatherSubService import WeatherSubService
from Service.CaiyunService import CaiyunService
from Instruction.Singleton import Singleton
from Model.DTO import Location, MsgToTG
from Instruction.TgBot import TgBot
import json
from Service.NewTgMsgSubject import NewTgMsgSubject
from datetime import datetime
from Instruction.Utils import Utils
from apscheduler.schedulers.background import BackgroundScheduler


@Singleton
class CornCore():
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.WeatherReportService = WeatherReportService()
    
    def run(self):
        self.scheduler.add_job(
            self.WeatherReportService.run,
            trigger='cron',
            minute=f'*/{Setting.CheckWeatherSchedule.value}'
            # second="*/20"
        )

@Singleton
class WeatherReportService():
    def __init__(self) -> None:
        self.cy = CaiyunService()
        self.bot = TgBot().get_bot()
        self.tgMsgSub = NewTgMsgSubject()
        pass

    def run(self):
        subs = WeatherSubService().listAll()
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
            isSentReport = self.processReport(user, ws, resultMsg)
            self.processAlert(user, ws, result, isSentReport)
            self.processForecastKeypoing(user, ws, result, isSentReport)

    def processReport(self, user: User, weatherSub: WeatherSub, resultMsg):
        nowTime = datetime.now().strftime("%H:%M")
        nowTime = datetime.strptime(nowTime,"%H:%M").time()
        reportTime = datetime.strptime(weatherSub.ReportTime,"%H:%M").time()
        diffMin = Utils().MinusTime(nowTime, reportTime)
        if(diffMin < Setting.CheckWeatherSchedule.value):
            msgToTG = MsgToTG(user.TgChatID, resultMsg)
            self.tgMsgSub.data = msgToTG
            return True
        return False
    
    def processAlert(self, user: User, weatherSub: WeatherSub, result, isSentReport = False):
        newAlert = result["alert"]["content"]
        newAlertStr = json.dumps(newAlert)
        if(newAlertStr == weatherSub.LastAlert):
            return
        alertMsg = self.cy.getAlertMsg(result)
        weatherSub.LastAlert = newAlertStr
        WeatherSubService().upsertByTgID(weatherSub)

        if(not alertMsg or isSentReport): return
        msgToTG = MsgToTG(user.TgChatID, alertMsg)
        self.tgMsgSub.data = msgToTG
    
    def processForecastKeypoing(self, user: User, weatherSub: WeatherSub, result, isSentReport = False):
        fk = result["forecast_keypoint"]
        if(fk == weatherSub.LastForecastKeyPoint):
            return
        weatherSub.LastForecastKeyPoint = fk
        WeatherSubService().upsertByTgID(weatherSub)

        if isSentReport: return
        msgToTG = MsgToTG(user.TgChatID, fk)
        self.tgMsgSub.data = msgToTG
