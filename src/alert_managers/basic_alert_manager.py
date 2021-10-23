from src.interfaces.abstract_alert_manager import AbstractAlertManager, AlertStatus, AlertInfo
from time import time
from typing import Optional


class BasicAlertManager(AbstractAlertManager):

    def __init__(self, traffic_limit: int):
        self.traffic_limit = traffic_limit
        self.status: AlertStatus = AlertStatus.NO_ALERT

    def get_alert_info(self, traffic: int) -> Optional[AlertInfo]:
        """
        Manages alert status, and emits alert information in case a threshold is crossed.
        :param traffic: current aggregated traffic information
        :return: alert_info in case threshold crossed ; None otherwise
        """
        emit_alert = False
        if self.status == AlertStatus.NO_ALERT:
            # traffic crosses over threshold
            if traffic > self.traffic_limit:
                self.status = AlertStatus.OVER_THRESHOLD
                emit_alert = True
        elif self.status == AlertStatus.OVER_THRESHOLD:
            # traffic crosses under threshold
            if traffic < self.traffic_limit:
                self.status = AlertStatus.UNDER_THRESHOLD
                emit_alert = True
        elif self.status == AlertStatus.UNDER_THRESHOLD:
            if traffic > self.traffic_limit:
                # traffic crosses over threshold again
                self.status = AlertStatus.OVER_THRESHOLD
                emit_alert = True
            else:
                # traffic is normal
                self.status = AlertStatus.NO_ALERT
        if emit_alert:
            return AlertInfo(status=self.status,
                             traffic_value=traffic,
                             timestamp=time())
        return None
