from Model.Enum import ConfigKey, Language
from .ConfigService import Config as conf
import requests
import json
import logging
from Model.Enum import skycon, LanguageList as ll
from Model.Language import LANG
from Model.DTO import Location

class CaiyunService():
    def __init__(self) -> None:
        self.url = "https://api.caiyunapp.com/v2.6"
        c = conf()
        self.token = c.getByKey(ConfigKey.Tokens.value, ConfigKey.CaiyunWeather.value)
    def check_by_location(self, location: Location):
        url = f"{self.url}/{self.token}/{location.longitude},{location.latitude}/weather?alert=true&dailysteps=1&hourlysteps=24"
        x = requests.get(url)
        result = json.loads(x.text)
        logging.info("Request weather report success: %s" % (x.text))
        return result['result']

    def getRainType(self, intensity, defaultSkycon, lang): # https://docs.caiyunapp.com/docs/tables/precip/
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
            return lang.l(ll[skycon[defaultSkycon].name])
        if 'RAIN' in defaultSkycon:
            type += '_RAIN'
            return lang.l(ll[skycon[type].name])
        if 'SNOW' in defaultSkycon:
            type += '_SNOW'
            return lang.l(ll[skycon[type].name])
        else:
            return lang.l(ll[skycon[defaultSkycon].name])

    def getRainMsg(self, precipitation, defaultSkycon, lang):
        rainType = ''
        intensity = precipitation['nearest']['intensity']
        rainType = self.getRainType(precipitation['nearest']['intensity'], defaultSkycon, lang)
        if(precipitation['local']['intensity'] >= 0.08): # local rain
            return (lang.l(ll.WR_RAIN_MSG_LOCAL) % (rainType, intensity))
        elif(precipitation['nearest']['intensity'] >= 0.08): # nearest rain
            if 'RAIN' in rainType:
                rainType = lang.l(ll.WR_RAIN_MSG_RAIN)
            elif 'SNOW' in rainType:
                rainType = lang.l(ll.WR_RAIN_MSG_SNOW)
            else:
                rainType = lang.l(ll.WR_RAIN_MSG_CLOUD)
            return (lang.l(ll.WR_RAIN_MSG) % (rainType, precipitation['nearest']['distance']))
        return (lang.l(ll.WR_RAIN_MSG_NO) % (rainType)) # no rain
    
    def getReportMsg(self, result, userLang):
        # try:
        lang = LANG(userLang)
        realtime = result['realtime']
        defaultSkycon = realtime['skycon']
        resultMsg = (lang.l(ll.WR_REPORT_MSG) % 
            (lang.l(ll[skycon[realtime['skycon']].name])
            , str(realtime['temperature'])
            , str(realtime['apparent_temperature'])
            , self.getRainMsg(realtime['precipitation'], defaultSkycon, lang)
            , str(realtime['humidity']*100)
            , realtime['air_quality']['description']['usa']
            , str(realtime['visibility'])))

        if(result["forecast_keypoint"]):
            resultMsg += result["forecast_keypoint"]

        lastAlert = ""
        if(len(result["alert"]["content"]) > 0):
            alertMsg = "\n❗ ❗ ❗\n"
            for alert in result["alert"]["content"]:
                desc = alert["description"]
                if(desc != lastAlert):
                    alertMsg += desc + "\n"
                    lastAlert = desc
            resultMsg += f"""\n{alertMsg}"""
                
        return resultMsg

    def getAlertMsg(self, result):
        lastAlert = ""
        if(len(result["alert"]["content"]) > 0):
            alertMsg = "\n❗ ❗ ❗\n"
            for alert in result["alert"]["content"]:
                desc = alert["description"]
                if(desc != lastAlert):
                    alertMsg += desc + "\n"
                    lastAlert = desc
        return alertMsg