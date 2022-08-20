from abc import ABC, abstractmethod
class ObserverABC(ABC):
    @abstractmethod
    def notify(self, data, *args, **kwargs):
        pass