class User():    
    def __init__(self, d=None) -> None:
        self.TgFirstName = ""
        self.TgName = ""
        self.TgID = ""
        self.TgChatID = ""
        self.PushDeerID = ""
        self.Language = ""
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    def IsInvalid(self):
        if(not self.TgId or self.TgId.isspace()):
            return False
        return True

class WeatherSub():
    def __init__(self, d=None) -> None:
        self.id = ""
        self.UserID = ""
        self.IsSubscribe = False
        self.IsSubAlert = True
        self.SubLongitude = 0
        self.SubLatitude = 0
        self.LastAlert = ""
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    def IsInvalid(self):
        if not self.UserID or self.UserID.isspace():
            return False
        return True