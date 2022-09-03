from sqlite_utils import Database
from Model.PO import WeatherSub
from Model.Enum import Setting, Language as langE
from Instruction.Singleton import Singleton

@Singleton
class WeatherSubService():
    def __init__(self) -> None:
        pass
    
    def isSubed(self, TgID):
        pass

    def isReachLimit(self, UserID):
        if None == UserID:
            return False

        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        count = table.count_where(f"UserID = :UserID", {"UserID": UserID})
        if count < Setting.MaxSubLimit.value:
            return False
        return True

    def upsertByTgID(self, sub: WeatherSub):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        sdic = sub.__dict__
        table.upsert(sdic, hash_id_columns=("UserID", "Longitude", "Latitude", "ReportTime"))
    
    def update(self, sub: WeatherSub):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        sdic = sub.__dict__
        table.update(sub.id, sdic)

    def listAll(self):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        allSubs = table.rows_where("IsSub = :IsSub", {"IsSub": True})
        return allSubs
    
    def listByUserID(self, userId):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        subs = table.rows_where("UserID = :UserID", {"UserID": userId})
        return subs
    
    def getByID(self, id: str) -> WeatherSub:
        db = Database(Setting.DBName.value)
        defaultSub = WeatherSub()
        defaultSub.id = None
        existSub = next(db.query(
            f"select *from {Setting.DBTableWeatherSub.value} where id = :id",
            {"id": id}
        ), defaultSub.__dict__)
        return WeatherSub(existSub)

    def delByID(self, id: str):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableWeatherSub.value]

        table.delete(id)