from abc import ABC, abstractmethod
import logging
class SubjectABC(ABC):
    def __init__(self):
        self.observers = []
    
    @abstractmethod
    def add(self, observer):
        pass

    @abstractmethod
    def remove(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass