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

