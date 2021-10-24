import curses
from typing import List
from .constants_view import HIGHEST_HITS_HEADER, ALERTS_HEADER
from src.interfaces.abstract_view import AbstractView, LIMIT_TOTAL_ALERT
from .constants_view import FORMAT_MSG_RECOVERED_ALERT, FORMAT_MSG_HIGH_ALERT
from src.interfaces.abstract_alert_manager import AlertStatus
from src.interfaces.abstract_collector import HitInfo
from datetime import datetime


class CursesView(AbstractView):

    def __init__(self):
        super().__init__()
        self.stdscr = curses.initscr()
        begin_hits_x = 0
        begin_y = 0
        height_hits = 11  # important since <-> max number of hits - 1
        height_alerts = LIMIT_TOTAL_ALERT + 1
        width = 120
        self.win_highest_hits = curses.newwin(height_hits, width, begin_hits_x, begin_y)
        self.win_alerts = curses.newwin(height_alerts, width, begin_hits_x + height_hits + 1, begin_y)
        self.win_highest_hits.clear()
        self.win_alerts.clear()

    def update_highest_hits(self, highest_hits: List[HitInfo]) -> None:
        self.win_highest_hits.clear()
        try:
            self.win_highest_hits.addstr(f'{HIGHEST_HITS_HEADER}\n')
            for highest_hit in highest_hits:
                self.win_highest_hits.addstr(f"{highest_hit}\n")
        except curses.error:
            pass
        self.win_highest_hits.refresh()

    def print_alert_info(self) -> None:
        self.win_alerts.clear()
        try:
            self.win_alerts.addstr(f'{ALERTS_HEADER}\n')
            for alert in self.all_alerts:
                dt = datetime.fromtimestamp(alert.timestamp)
                if alert.status == AlertStatus.OVER_THRESHOLD:
                    self.win_alerts.addstr(FORMAT_MSG_HIGH_ALERT % (str(alert.traffic_value), str(dt)))
                    self.win_alerts.addstr('\n')
                elif alert.status == AlertStatus.UNDER_THRESHOLD:
                    self.win_alerts.addstr(FORMAT_MSG_RECOVERED_ALERT % (str(alert.traffic_value), str(dt)))
                    self.win_alerts.addstr('\n')
        except curses.error:
            pass
        self.win_alerts.refresh()
