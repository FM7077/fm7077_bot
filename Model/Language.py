from enum import Enum
from Model.Enum import Language as langE

class LANG():
    def __init__(self, lang = langE.ENG) -> None:
        self.lang = lang
        pass
    def l(self, code):
        if(self.lang == langE.ENG):
            return ENG[code.name].value
        return ENG[code.name].value # return english by default

class ENG(Enum):
    OPT_WR_MINUTELY = "Minutely⏲"
    OPT_WR_HOURLY = "Hourly🕰️"
    OPT_WR_DAILY = "Daily 🗓️"
    OPT_WR_REALTIME = "Realtime"

    SUB_WR_CHO_LOC = "Let me help you to subscribe the weather report.\n\nFirst, please send me the location. 📌"
    SUB_WR_SET_NAME = "Now please set the name"
    SUB_WR_EMP_NAME = "The name cant be empty please resend one"
    SUB_WR_CHO_TIME_Hour = "Now please set the report time _ _ : _ _ 🔔"
    SUB_WR_CHO_TIME_MINUTE = "Now please set the report time *%s* : _ _ 🔔" # (hour)
    SUB_WR_CHO_CONFIRM = "Please check the location and the time are correct. *%s* 🔎\n\nIf you want to change location or time, just input /cancel and resend /subweather." #(time)
    SUB_WR_SET = "Congratulation, the *subscription* %s is set.\nI'll sent you a daily report at *%s* ✔️" # (name, time)
    SUB_WR_CANCEL = "No subscription will be set ❌"
    SUB_WR_UNKNOWN_MSG = "You should finish the subscription or /cancel current job"
    SUB_WR_REACH_LIMIT = "Sorry, but you reach the subscription limit %s" # (limit)

    WR_REPORT_MSG = """Here is the realtime weather for you:
%s\n
Temperature: %s°C, apparent: %s°C\n
Rain: %s\n
Humidity: %s%%\n
Air quality: %s, visibility: %sKm\n""" # (skycon, temperature, apparent_temperature, rainMsg, humidity, air_quality, visibility)
    WR_RAIN_MSG = "the nearest %s is %sKm away" # (rainType, distance)
    WR_RAIN_MSG_LOCAL = "Its %s %smm/h now" # (rainType, intensity)
    WR_RAIN_MSG_NO = "Its %s now" # (rainType)
    WR_RAIN_MSG_RAIN = "rain cloud 🌧️"
    WR_RAIN_MSG_SNOW = "snow cloud ❄️"
    WR_RAIN_MSG_CLOUD = "cloud ☁️"
    
    CLEAR_DAY = "Clear day ☀️",
    CLEAR_NIGHT = "Clear night 🌕"
    PARTLY_CLOUDY_DAY = "Partly cloudy day 🌤️"
    PARTLY_CLOUDY_NIGHT = "Partly cloudy night ☁️🌓"
    CLOUDY = "Cloudy ☁️☁️"
    LIGHT_HAZE = "Light haze 🌫️"
    MODERATE_HAZE = "Moderate haze 😶‍🌫️"
    HEAVY_HAZE = "Heavy haze 😷🌫️"
    LIGHT_RAIN = "Light rain 🌦️"
    MODERATE_RAIN = "Moderate rain 🌧️"
    HEAVY_RAIN = "Heavy rain 🌧️🌧️"
    STORM_RAIN = "Storm rain ⛈️"
    FOG = "Fog ☁️🌫️"
    LIGHT_SNOW = "Light snow ❄️"
    MODERATE_SNOW = "Moderate snow ❄️❄️"
    HEAVY_SNOW = "Heavy snow ❄️❄️❄️"
    STORM_SNOW = "Storm snow ❄️❄️❄️❄️"
    DUST = "Dust"
    SAND = "Sand"
    WIND = "Wind"

    MSG_GOT_LOC = "Hi %s, got your location, now I will check weather report for you" #(username)

    ERR_MSG = "Sorry, it seems something went wrong"

    BUT_CONFIRM = "Confirm"
    BUT_CANCEL = "Cancel"