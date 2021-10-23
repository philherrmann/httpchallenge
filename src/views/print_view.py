from typing import List
from src.interfaces.abstract_alert_manager import AlertInfo, AlertStatus
from src.interfaces.abstract_view import AbstractView
from src.interfaces.abstract_collector import HitInfo
from datetime import datetime
from .constants_view import TOTAL_TRAFFIC, HIGHEST_HITS

LIMIT_TOTAL_ALERT = 10  # limit on the maximum number of alerts kept in history


class PrintView(AbstractView):

    def __init__(self):
        self.all_alerts: List[AlertInfo] = []

    def update_highest_hits(self, highest_hits: List[HitInfo]) -> None:
        print(f"{HIGHEST_HITS}:")
        for highest_hit in highest_hits:
            print(f"{highest_hit}")

    def update_traffic(self, total_traffic: int) -> None:
        print(f"{TOTAL_TRAFFIC}: {total_traffic}")

    def update_alert_info(self, alert_info: AlertInfo) -> None:
        if alert_info.status == AlertStatus.NO_ALERT:
            pass
        self.all_alerts.append(alert_info)
        if len(self.all_alerts) > LIMIT_TOTAL_ALERT:
            self.all_alerts = self.all_alerts[-LIMIT_TOTAL_ALERT:]

    def print_alert_info(self) -> None:
        for alert in self.all_alerts:
            dt = datetime.fromtimestamp(alert.timestamp)
            if alert.status == AlertStatus.OVER_THRESHOLD:
                print(f"High traffic generated an alert - hits = {alert.traffic_value}, triggered at {dt}")
            elif alert.status == AlertStatus.UNDER_THRESHOLD:
                print(f"Traffic recovered - hits = {alert.traffic_value}, triggered at {dt}")
