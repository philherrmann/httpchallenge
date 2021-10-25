from src.interfaces.abstract_collector import AbstractCollector, HitInfo, HTTPInfo
from dataclasses import dataclass
from typing import List, Dict
from time import time


@dataclass(frozen=True)
class TrafficInfo:
    """
    Used only internally to this module.
    """
    timestamp: float
    traffic_len: int


class BasicCollector(AbstractCollector):

    def __init__(self, history_span: int = 120):
        """
        Collect traffic information.
        :param history_span: number of seconds history of traffic is kept
        """
        self.http_container: Dict[str, HitInfo] = dict()
        self.total_traffic = 0
        self.traffic_history: List[TrafficInfo] = []
        self.history_span = history_span

    def get_total_traffic(self) -> int:
        return self.total_traffic

    def get_highest_hits(self) -> List[HitInfo]:
        """
        Return highest hits sorted by number of hits
        :return:
        """
        hits: List[HitInfo] = list(self.http_container.values())
        return sorted(hits, key=lambda hit_info: -hit_info.nb_hits)

    def collect_http_info(self, http_info: HTTPInfo) -> None:
        section = http_info.extract_section()
        if section in self.http_container:
            current_hit_info: HitInfo = self.http_container[section]
            self.http_container[section] = current_hit_info.add(section, http_info)
        else:
            self.http_container[section] = HitInfo().add(section, http_info)
        content_length = http_info.content_length
        self.total_traffic += content_length
        self.__add_to_traffic_history(content_length)

    def clear(self, clear_history:bool = False) -> None:
        self.http_container.clear()
        self.total_traffic = 0
        if clear_history:
            self.traffic_history = []

    def __add_to_traffic_history(self, traffic_len: int) -> None:
        current_timestamp: float = time()
        self.traffic_history.append(TrafficInfo(timestamp=current_timestamp, traffic_len=traffic_len))
        self.traffic_history = \
            list(filter(lambda traffic_info: traffic_info.timestamp > current_timestamp - self.history_span,
                        self.traffic_history))

    def get_total_traffic_over_period(self, span: int) -> int:
        current_timestamp: float = time()
        return sum([traffic_info.traffic_len for traffic_info in
                    filter(lambda traffic_info: traffic_info.timestamp >= current_timestamp - span,
                           self.traffic_history)])
