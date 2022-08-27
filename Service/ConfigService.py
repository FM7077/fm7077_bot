from Instruction.Singleton import Singleton
import configparser

@Singleton
class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
    def getByKey(self, section, key):
        return self.config.get(section, key)
    def getBySection(self, option):
        return self.config.items(option)