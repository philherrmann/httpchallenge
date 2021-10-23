from abc import ABC, abstractmethod
from typing import List
from src.interfaces.abstract_alert_manager import AlertInfo
from src.interfaces.abstract_collector import HitInfo


class AbstractView(ABC):

    @abstractmethod
    def update_highest_hits(self, highest_hits: List[HitInfo]) -> None:
        '''
        Update highest hits in view
        '''

    @abstractmethod
    def update_traffic(self, total_traffic: int) -> None:
        '''
        Update traffic in view
        '''

    @abstractmethod
    def update_alert_info(self, alert_info: AlertInfo) -> None:
        '''
        Update alert information (no display, see print_alert_info for this)
        :param alert_info: input alert_info
        '''

    @abstractmethod
    def print_alert_info(self) -> None:
        '''
        Displays alerts history
        '''