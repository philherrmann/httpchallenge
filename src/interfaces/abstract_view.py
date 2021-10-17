from abc import ABC, abstractmethod


class AbstractView(ABC):

    @abstractmethod
    def update(self, info: str):
        '''
        Update the view
        :param info:
        :return:
        '''