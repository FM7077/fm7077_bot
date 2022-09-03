from enum import Enum
from Model.Enum import Language as langE, TgCommand

class LANG():
    def __init__(self, lang = langE.ENG) -> None:
        self.lang = lang
        pass
    def l(self, code):
        if(self.lang == langE.ENG):
            return ENG[code.name].value
        return ENG[code.name].value # return english by default

class ENG(Enum):
    WELCOME = "Hi %s nice to meet you"
    HELP = f"""Hi %s let me show you what I can do:\n
Send me a location directly, and I can tell you what weather forecast\n
/{TgCommand.SUBWEATHER.value}: subscribe a new weather report\n
/{TgCommand.MYSUBS.value}: check your subscriptions\n
I can not only send you daily weather report, but also can send you alert when there is one"""

    OPT_WR_MINUTELY = "Minutely⏲"
    OPT_WR_HOURLY = "Hourly🕰️"
    OPT_WR_DAILY = "Daily 🗓️"
    OPT_WR_REALTIME = "Realtime"

    SUB_WR_ACT_SUB = "subscribe the weather report"
    SUB_WR_ACT_UPDATE = "update the subscription "
    SUB_WR_CHO_LOC = "Let me help you to %s%s.\n\nFirst, please send me the location. 📌" # (action, Name)
    SUB_WR_SET_NAME = "Now please set the name"
    SUB_WR_EMP_NAME = "The name cant be empty please resend one"
    SUB_WR_CHO_TIME_Hour = "Now please set the report time _ _ : _ _ 🔔"
    SUB_WR_CHO_TIME_MINUTE = "Now please set the report time *%s* : _ _ 🔔" # (hour)
    SUB_WR_CHO_CONFIRM = "Please check the location and the time are correct. *%s* 🔎\n\nIf you want to change location or time, just input /cancel and resend /subweather." #(time)
    SUB_WR_SET = "Congratulation, the *subscription* %s is set.\nI'll sent you a daily report at *%s* ✔️" # (name, time)
    SUB_WR_CANCEL = "No subscription will be set or changed ❌"
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
    
    CLEAR_DAY = "Clear day ☀️"
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

    BTN_CONFIRM = "Confirm"
    BTN_CANCEL = "Cancel"

    NO_SUB = f"You have no subscription yet, /{TgCommand.SUBWEATHER.value} to subscribe one"
    HAS_SUBS = "Here are your subscriptions:"
    DEL_SUB = "Are you sure deleting?"
    BTN_ED_SUB = "Edit ✍️"
    BTN_DEL_SUB = "Delete 🗑️"
    BTN_BACK_SUB_LIST = "<< Back to subscriptions"
    BTN_DELSUB_CONFIRM = "Delete 🗑️"
    BTN_DELSUB_CANCEL = "<< Cancel"
    SUB_DETAIL = """Here is the info of %s\n
Location: %s, %s\n
Is send daily report: %s\n
daily report time: %s\n
Is subscribe weather alert: %s\n
""" # (Name, longitude, latitude, IsSub, ReportTime, IsSubALret)