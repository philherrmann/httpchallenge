from abc import ABC, abstractmethod


class AbstractSniffer(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass