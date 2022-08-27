class Location():
    def __init__(self, longitude: float, latitude: float) -> None:
        self.longitude = longitude
        self.latitude = latitude
class MsgToTG():
    def __init__(self, chatId, msg) -> None:
        self.chatId = chatId
        self.msg = msg