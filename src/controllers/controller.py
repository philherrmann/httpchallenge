import time

from threading import Event
from src.collectors.basic_collector import BasicCollector
from src.sniffers.snappy_sniffer import SnappySniffer
from src.interfaces.abstract_view import AbstractView
from src.types.http_info import HTTPInfo


class Controller:

    def __init__(self, view: AbstractView):
        self.http_collector = BasicCollector()
        self.sniffer = SnappySniffer(receive_http_callback=lambda http_info: self._receive_http_callback(http_info))
        self.view = view
        self.stop_event = Event()

    def _receive_http_callback(self, http_info: HTTPInfo):
        self.http_collector.collect_http_info(http_info)

    def start(self):
        self.sniffer.start()
        while not self.stop_event.is_set():
            time.sleep(10)
            self._update_view()

    def _update_view(self):
        current_results = dict(self.http_collector.http_container)
        all_results = list(current_results.keys())
        self.view.update_highest_hits(all_results)
        self.view.update_traffic(self.http_collector.total_content_length)
        self.http_collector.clear()

    def stop(self):
        self.stop_event.set()
        self.sniffer.stop()
