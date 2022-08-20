from Abstraction.ObserverABC import ObserverABC
from Abstraction.SubjectABC import SubjectABC
from Service.Config import Config as conf
from Service.NewTgMsgObserver import NewTgMsgObserver
from Instruction.Singlton import Singleton
import logging

@Singleton
class NewTgMsgSubject(SubjectABC):
    """具体主题（具体目标类）"""

    def __init__(self):
        # super().__init__()
        self._data = None
        self.observers = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        """当数据更新时，去通知观察者"""
        self._data = new_data
        self.notify()
    
    def add(self, observer):
        pass
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            logging.error("%s observer is exist, add failed" % observer)

    def remove(self, observer):
        pass
        if observer in self.observers:
            self.observers.remove(observer)
        else:
            logging.error("%s observer is not exist, remove failed" % observer)

    def notify(self):
        """通知观察者的具体方法"""
        for obs in self.observers:
            obs.notify(self._data)