from Model.Enum import Language
class User():    
    def __init__(self, d=None) -> None:
        self.TgID = ""
        self.TgChatID = ""
        self.TgName = ""
        self.TgFirstName = ""
        self.Language = Language.ENG.name
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)
            self.id = d["id"]

    def IsInvalid(self):
        if(not self.TgID or self.TgID < 1):
            return True
        return False

class WeatherSub():
    def __init__(self, d=None) -> None:
        self.UserID = ""
        self.Name = ""
        self.IsSub = True
        self.IsSubAlert = True
        self.Longitude = 0
        self.Latitude = 0
        self.LastAlert = ""
        self.ReportTime = ""
        self.LastForecastKeyPoint = ""
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    def IsInvalid(self):
        if not self.UserID or self.UserID.isspace():
            return False
        return True