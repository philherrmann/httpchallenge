from abc import ABC, abstractmethod
from typing import List
from src.interfaces.abstract_alert_manager import AlertInfo, AlertStatus
from src.interfaces.abstract_collector import HitInfo

LIMIT_TOTAL_ALERT = 10  # limit on the maximum number of alerts kept in history


class AbstractView(ABC):

    def __init__(self):
        self.all_alerts: List[AlertInfo] = []

    @abstractmethod
    def update_highest_hits(self, highest_hits: List[HitInfo]) -> None:
        '''
        Update highest hits in view
        '''

    @abstractmethod
    def print_alert_info(self) -> None:
        '''
        Displays alerts history
        '''

    def update_alert_info(self, alert_info: AlertInfo) -> None:
        '''
        Update list of alerts - common to all subclasses (cf. print_alert_info has to be implemented)
        :param alert_info:
        :return:
        '''
        if alert_info.status == AlertStatus.NO_ALERT:
            pass
        self.all_alerts.append(alert_info)
        if len(self.all_alerts) > LIMIT_TOTAL_ALERT:
            self.all_alerts = self.all_alerts[-LIMIT_TOTAL_ALERT:]