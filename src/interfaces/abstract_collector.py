from abc import ABC, abstractmethod
from src.types.http_info import HTTPInfo


class AbstractCollector(ABC):

    @abstractmethod
    def collect_http_info(self, http_info: HTTPInfo):
        '''
        Collect HTTP request info
        :param http_info:
        :return:
        '''