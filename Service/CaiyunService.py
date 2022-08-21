from Model.Enum import ConfigKey, Language
from .Config import Config as conf
import requests
import json
import logging
from Model.Enum import skycon

class CaiyunService():
    def __init__(self) -> None:
        self.url = "https://api.caiyunapp.com/v2.6"
        c = conf()
        self.token = c.getByKey(ConfigKey.Tokens.value, ConfigKey.CaiyunWeather.value)
    def check_by_location(self, location):
        self.url += "/%s/%s/weather?alert=true&dailysteps=1&hourlysteps=24" % (self.token, str(location.longitude) + ',' + str(location.latitude))
        x = requests.get(self.url)
        result = json.loads(x.text)
        logging.info("Request weather report success: %s" % (x.text))
        return result['result']

    def get_rain_type(self, intensity, defaultSkycon): # https://docs.caiyunapp.com/docs/tables/precip/
        type = ''
        if(intensity >= 0.08 and intensity < 3.44):
            type = 'LIGHT'
        if(intensity >= 3.44 and intensity < 11.33):
            type = 'MODERATE'
        if(intensity >= 11.33 and intensity < 51.3):
            type = 'HEAVY'
        if(intensity >= 51.3):
            type = 'STORM'

        if(type == ''):
            return skycon[defaultSkycon].value
        if 'RAIN' in defaultSkycon:
            type += '_RAIN'
            return skycon[type].value
        if 'SNOW' in defaultSkycon:
            type += '_SNOW'
            return skycon[type].value
        else:
            return skycon[defaultSkycon].value

    def get_rain_msg(self, precipitation, defaultSkycon):
        local = ''
        nearest = ''
        if(precipitation['local']['intensity'] >= 0.08):
            return f"""Its {self.get_rain_type(precipitation['local']['intensity'], defaultSkycon)} ({precipitation['local']['intensity']}mm/h) now"""
        elif(precipitation['nearest']['intensity'] >= 0.08):
            nearest = self.get_rain_type(precipitation['nearest']['intensity'], defaultSkycon)
            if 'RAIN' in nearest:
                nearest = 'rain cloud 🌧️'
            elif 'SNOW' in nearest:
                nearest = 'snow cloud ❄️'
            else:
                nearest = 'cloud ☁️'
            return f"""the nearest {nearest} is {precipitation['nearest']['distance']}Km away"""
        return 'is no rain now'
    
    def getReportMsg(self, result, lang = Language.Eng):
        try:
            realtime = result['realtime']
            defaultSkycon = realtime['skycon']
            resultMsg = f"""
    Here is the realtime weather for you:
    {skycon[realtime['skycon']].value}\n
    Temperature: {realtime['temperature']}°C, apparent: {realtime['apparent_temperature']}°C\n
    Rain: {CaiyunService().get_rain_msg(realtime['precipitation'], defaultSkycon)}\n
    Humidity: {realtime['humidity']*100}%\n
    Air quality: {realtime['air_quality']['description']['usa']}, visibility: {realtime['visibility']}Km
            """

            if(result["forecast_keypoint"]):
                resultMsg += f"""\n{result["forecast_keypoint"]}"""

            lastAlert = ""
            if(len(result["alert"]["content"]) > 0):
                alertMsg = "❗ ❗ ❗\n"
                for alert in result["alert"]["content"]:
                    desc = alert["description"]
                    if(desc != lastAlert):
                        alertMsg += desc + "\n"
                        lastAlert = desc
                resultMsg += f"""\n{alertMsg}"""
                    
            return resultMsg
            
        except Exception as ex:
            logging.error(ex)
            return "Sorry but something went wrong"
