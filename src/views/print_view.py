from typing import List
from src.interfaces.abstract_alert_manager import AlertInfo, AlertStatus
from src.interfaces.abstract_view import AbstractView
from .constants_view import FORMAT_MSG_RECOVERED_ALERT, FORMAT_MSG_HIGH_ALERT
from src.interfaces.abstract_collector import HitInfo
from datetime import datetime
from .constants_view import HIGHEST_HITS_HEADER


class PrintView(AbstractView):

    def __init__(self):
        super().__init__()
        self.all_alerts: List[AlertInfo] = []

    def update_highest_hits(self, highest_hits: List[HitInfo]) -> None:
        print(f"{HIGHEST_HITS_HEADER} @ {datetime.now()}")
        for highest_hit in highest_hits:
            print(f"{highest_hit}")

    def print_alert_info(self) -> None:
        # don't use alerts header
        for alert in self.all_alerts:
            dt = datetime.fromtimestamp(alert.timestamp)
            if alert.status == AlertStatus.OVER_THRESHOLD:
                print(FORMAT_MSG_HIGH_ALERT % (str(alert.traffic_value), str(dt)))
            elif alert.status == AlertStatus.UNDER_THRESHOLD:
                print(FORMAT_MSG_RECOVERED_ALERT % (str(alert.traffic_value), str(dt)))

