import curses
from typing import List
from .constants_view import TOTAL_TRAFFIC, HIGHEST_HITS
from src.interfaces.abstract_view import AbstractView


class CursesView(AbstractView):

    def __init__(self):
        self.stdscr = curses.initscr()
        begin_x = 0
        begin_y = 0
        height = 11  # important since <-> max number of hits - 1
        width = 80
        self.win_highest_hits = curses.newwin(height, width, begin_y, begin_x)
        self.win_traffic = curses.newwin(1, width, begin_y + height + 1, begin_x)
        self.update_highest_hits("")
        self.update_traffic("0")

    def update_highest_hits(self, infos: List[str]):
        self.win_highest_hits.clear()
        try:
            self.win_highest_hits.addstr(f"{HIGHEST_HITS}")
            for info in infos:
                self.win_highest_hits.addstr(f"\n{info}")
        except curses.error:
            pass
        self.win_highest_hits.refresh()

    def update_traffic(self, info):
        self.win_traffic.clear()
        self.win_traffic.addstr(f"{TOTAL_TRAFFIC}: {info}")
        self.win_traffic.refresh()

