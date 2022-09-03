from enum import Enum

class DeerMsgTypeEnum(Enum):
    Text = "Text",
    Markdown = "Markdown",
    Image = "Image",

class ConfigKey(Enum):
    Tokens = "Tokens"
    Tg_Bot = "Tg_Bot"
    CaiyunWeather = "CaiyunWeather"

class Setting(Enum):
    DBName = "Bot.db"
    DBTableUser = "User"
    DBTableWeatherSub = "WeatherSub"
    
    MaxSubLimit = 5 # max subscription limit per user

    CheckWeatherSchedule = 5 # period time to check weather, minute

class skycon(Enum): # weather phenomenon https://docs.caiyunapp.com/docs/tables/skycon
    CLEAR_DAY = "CLEAR_DAY",
    CLEAR_NIGHT = "CLEAR_NIGHT"
    PARTLY_CLOUDY_DAY = "PARTLY_CLOUDY_DAY"
    PARTLY_CLOUDY_NIGHT = "PARTLY_CLOUDY_NIGHT"
    CLOUDY = "CLOUDY"
    LIGHT_HAZE = "LIGHT_HAZE"
    MODERATE_HAZE = "MODERATE_HAZE"
    HEAVY_HAZE = "HEAVY_HAZE"
    LIGHT_RAIN = "LIGHT_RAIN"
    MODERATE_RAIN = "MODERATE_RAIN"
    HEAVY_RAIN = "HEAVY_RAIN"
    STORM_RAIN = "STORM_RAIN"
    FOG = "FOG"
    LIGHT_SNOW = "LIGHT_SNOW"
    MODERATE_SNOW = "MODERATE_SNOW"
    HEAVY_SNOW = "HEAVY_SNOW"
    STORM_SNOW = "STORM_SNOW"
    DUST = "DUST"
    SAND = "SAND"
    WIND = "WIND"

class Language(Enum):
    ENG = "English"
    CNT = "Chinese Tractional"
    CHS = "Chinese Simple"

class LanguageList(Enum):
    WELCOME = "welcome word"
    HELP = "help word"

    OPT_WR_MINUTELY = "weather report option: minutely"
    OPT_WR_HOURLY = "weather report option hourly"
    OPT_WR_DAILY = "weather report option daily"
    OPT_WR_REALTIME = "weather report option realtime"

    SUB_WR_ACT_SUB = "subscribe"
    SUB_WR_ACT_UPDATE = "update"
    SUB_WR_CHO_LOC = "subscribe weather: choose location" # (action)
    SUB_WR_SET_NAME = "subscribe weather: set name"
    SUB_WR_EMP_NAME = "subscribe weather: name is empty"
    SUB_WR_CHO_TIME_Hour = "subscribe weather: choose hour"
    SUB_WR_CHO_TIME_MINUTE = "subscribe weather: choose minute"
    SUB_WR_CHO_CONFIRM = "subscribe weather: confirm"
    SUB_WR_SET = "subscribe weather: set"
    SUB_WR_CANCEL = "cancel subscription"
    SUB_WR_UNKNOWN_MSG = "unknown msg"
    SUB_WR_REACH_LIMIT = "reach limit"

    WR_REPORT_MSG = "weather report message"
    WR_RAIN_MSG = "weather report rain message"
    WR_RAIN_MSG_LOCAL = "weather report rain message: local rain"
    WR_RAIN_MSG_NO = "weather report rain message: no rain"
    WR_RAIN_MSG_RAIN = "weather report rain message: rain cloud"
    WR_RAIN_MSG_SNOW = "weather report rain message: snow cloud"
    WR_RAIN_MSG_CLOUD = "weather report rain message: cloud"
    
    CLEAR_DAY = "Clear day ☀️",
    CLEAR_NIGHT = "Clear night 🌕"
    PARTLY_CLOUDY_DAY = "Partly cloudy day 🌤️"
    PARTLY_CLOUDY_NIGHT = "Partly cloudy night ☁️🌓"
    CLOUDY = "Cloudy ☁️🌑"
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

    MSG_GOT_LOC = "got location message"

    ERR_MSG = "error msg"

    BTN_CONFIRM = "inline button: confirm"
    BTN_CANCEL = "inline button: cancel"

    NO_SUB = "user no sub yet"
    HAS_SUBS = "user has subs"
    DEL_SUB = "delete sub"
    BTN_ED_SUB = "Edit ✍️"
    BTN_DEL_SUB = "Delete 🗑️"
    BTN_BACK_SUB_LIST = "<< Back to subscriptions"
    SUB_DETAIL = "sub detail"

class TgCallBackType(Enum):
    OPT_WR_START = "OPTWR_"
    OPT_WR_MINUTELY = "OPTWR_MIN"
    OPT_WR_HOURLY = "OPTWR_HOU"
    OPT_WR_DAILY = "OPTWR_DL"
    OPT_WR_REALTIME = "OPTWR_RT"
    OPT_WR_EDIT = "OPTWR_ED"

    SUB_WR_SETH = "SUBWR_SETH"
    SUB_WR_SETM = "SUBWR_SETM"
    SUB_WR_CONFIRM = "SUBWR_CONFIRM"
    SUB_WR_CANCEL = "SUBWR_CANCEL"
    SUB_WR_DETAIL = "SUBWR_DT"
    SUB_WR_EDIT = "SUBWR_ED"
    SUB_WR_DELETE = "SUBWR_DE"
    LIST_SUBS = "LIST_SUBS"
    SUB_WR_DEL_CONFIRM = "SUBWR_DC"
    SUB_WR_DEL_CANCEL = "SUBWR_CD"

class TgCommand(Enum):
    START = "start",
    CHECKRAIN = "checkRain"
    SUBWEATHER = "subweather"
    CANCEL = "cancel"
    MYSUBS = "mysubs"
    HELP = "help"
