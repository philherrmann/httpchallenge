from abc import ABC, abstractmethod
from typing import List


class AbstractView(ABC):

    @abstractmethod
    def update_highest_hits(self, infos: List[str]):
        '''
        Update highest hits in view
        '''

    @abstractmethod
    def update_traffic(self, info):
        '''
        Update traffic in view
        '''