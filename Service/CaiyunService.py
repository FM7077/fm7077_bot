from Model.Enum import ConfigKey
from .Config import Config as conf
import requests
import json

class CaiyunService():
    def __init__(self) -> None:
        self.url = "https://api.caiyunapp.com/v2.6"
        c = conf()
        self.token = c.getByKey(ConfigKey.Tokens.value, ConfigKey.CaiyunWeather.value)
    def check_by_location(self, location):
        self.url += "/%s/%s/realtime" % (self.token, str(location.longitude) + ',' + str(location.latitude))
        x = requests.get(self.url)
        result = json.loads(x.text)
        return result['result']['realtime']
