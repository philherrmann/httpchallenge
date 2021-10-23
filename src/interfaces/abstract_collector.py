from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.types.http_info import HTTPInfo


@dataclass(frozen=True)
class HitInfo:

    section: str
    nb_hits: int
    traffic: int

    def __repr__(self):
        return f"{self.section}: hits {self.nb_hits} | total traffic {self.traffic}"


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
        Clear total traffic information
        :param clear_history: also clear history of traffic
        """

    @abstractmethod
    def get_total_traffic_over_period(self, span: int) -> int:
        """
        Get total traffic over the last "span" seconds (or up to traffic history span)
        :param span: duration in seconds over which traffic should be computed.
        :return: total traffic over period
        """
