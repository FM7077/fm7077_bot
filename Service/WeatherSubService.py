from sqlite_utils import Database
from Model.PO import WeatherSub
from Model.Enum import Setting, Language as langE
from Instruction.Singleton import Singleton

@Singleton
class WeatherSubService():
    def __init__(self) -> None:
        pass
    
    def IsSubed(self, TgID):
        pass

    def IsReachLimit(self, UserID):
        if None == UserID:
            return False

        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        count = table.count_where(f"UserID = :UserID", {"UserID": UserID})
        if count < Setting.MaxSubLimit.value:
            return False
        return True

    def UpsertByTgID(self, sub):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        sdic = sub.__dict__
        table.upsert(sdic, hash_id_columns=("UserID", "Longitude", "Latitude", "ReportTime"))

    def ListAll(self):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        allSubs = table.rows_where("IsSub = :IsSub", {"IsSub": True})
        return allSubs