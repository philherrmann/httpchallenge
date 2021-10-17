from typing import List
from src.interfaces.abstract_view import AbstractView
from .constants_view import TOTAL_TRAFFIC, HIGHEST_HITS


class PrintView(AbstractView):

    def update_highest_hits(self, infos: List[str]):
        print(f"{HIGHEST_HITS}:")
        for info in infos:
            print(f"{info}")

    def update_traffic(self, info):
        print(f"{TOTAL_TRAFFIC}: {info}")