from typing import List
from time import time
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPInfo:

    method: str  # make it an enum
    host: str
    path: str
    content_length: int

    def extract_section(self):
        return self.host + '/'.join(self.path.split('/', 2)[:2])


@dataclass(frozen=True)
class HitInfo:

    section: str = ""
    nb_hits: int = 0
    traffic: int = 0
    last_hit_traffic: int = 0
    last_hit_timestamp: float = 0.0

    def add(self, section: str, http_info: HTTPInfo): # -> HitInfo:
        return HitInfo(section=section,
                       nb_hits=self.nb_hits + 1,
                       traffic=self.traffic + http_info.content_length,
                       last_hit_traffic=http_info.content_length,
                       last_hit_timestamp=time())

    def __repr__(self):
        last_dt = datetime.fromtimestamp(self.last_hit_timestamp)
        return f"{self.section}: hits {self.nb_hits} | total traffic {self.traffic} " \
               f"| last request traffic {self.last_hit_traffic} @ {last_dt}"


class AbstractCollector(ABC):

    @abstractmethod
    def get_total_traffic(self) -> int:
        """
        Returns total traffic over the past X minutes (default 2 minutes)
        :return:
        """

    @abstractmethod
    def get_highest_hits(self) -> List[HitInfo]:
        """
        Return highest hits as sections
        :return:
        """

    @abstractmethod
    def collect_http_info(self, http_info: HTTPInfo) -> None:
        """
        Collect HTTP traffic information
        :param http_info: HTTP traffic information
        """

    @abstractmethod
    def clear(self, clear_history: bool = False) -> None:
        """
        Clear traffic information.
        :param clear_history: also clear history of traffic
        """

    @abstractmethod
    def get_total_traffic_over_period(self, span: int) -> int:
        """
        Get total traffic over the last "span" seconds (or up to traffic history span)
        :param span: duration in seconds over which traffic should be computed.
        :return: total traffic over period
        """
