from src.interfaces.abstract_collector import AbstractCollector
from src.types.http_info import HTTPInfo
from collections import defaultdict


class BasicCollector(AbstractCollector):

    def __init__(self):
        self.http_container = defaultdict(list)
        self.total_content_length = 0

    def collect_http_info(self, http_info: HTTPInfo):
        self.http_container[http_info.host].append(http_info)
        self.total_content_length += http_info.content_length

    def clear(self):
        self.http_container.clear()
        self.total_content_length = 0