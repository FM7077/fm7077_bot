from enum import Enum

class DeerMsgTypeEnum(Enum):
    Text = "Text",
    Markdown = "Markdown",
    Image = "Image",

class ConfigKey(Enum):
    Tokens = "Tokens"
    PushDeer_FM7077 = "PushDeer_FM7077"
    Tg_Bot = "Tg_Bot"
    CaiyunWeather = "CaiyunWeather"

class Setting(Enum):
    DBName = "Bot.db"
    DBTableUser = "User"
    DBTableWeatherSub = "WeatherSub"

class skycon(Enum): # weather phenomenon https://docs.caiyunapp.com/docs/tables/skycon
    CLEAR_DAY = "clear day ☀️",
    CLEAR_NIGHT = "clear night 🌕"
    PARTLY_CLOUDY_DAY = "partly cloudy day 🌤️"
    PARTLY_CLOUDY_NIGHT = "partly cloudy night ☁️🌓"
    CLOUDY = "cloudy ☁️🌑"
    LIGHT_HAZE = "light haze 🌫️"
    MODERATE_HAZE = "moderate haze 😶‍🌫️"
    HEAVY_HAZE = "heavy haze 😷🌫️"
    LIGHT_RAIN = "light rain 🌦️"
    MODERATE_RAIN = "moderate rain 🌧️"
    HEAVY_RAIN = "heavy rain 🌧️🌧️"
    STORM_RAIN = "storm rain ⛈️"
    FOG = "fog ☁️🌫️"
    LIGHT_SNOW = "light snow ❄️"
    MODERATE_SNOW = "moderate snow ❄️❄️"
    HEAVY_SNOW = "heavy snow ❄️❄️❄️"
    STORM_SNOW = "storm snow ❄️❄️❄️❄️"
    DUST = "dust"
    SAND = "sand"
    WIND = "wind"

class Language(Enum):
    Eng = "English"
    CNT = "Chinese Tractional"
    CHS = "Chinese Simple"

class TgCallBackType(Enum):
    OPT_WR_START = "OPTWR_"
    OPT_WR_MINUTELY = "OPTWR_MIN"
    OPT_WR_HOURLY = "OPTWR_HOU"
    OPT_WR_DAILY = "OPTWR_DL"
    OPT_WR_REALTIME = "OPTWR_RT"
