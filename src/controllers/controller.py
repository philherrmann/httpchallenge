import time

from threading import Event
from typing import Optional
from src.alert_managers.basic_alert_manager import BasicAlertManager, AlertInfo
from src.collectors.basic_collector import BasicCollector
from src.sniffers.scapy_sniffer import ScapySniffer
from src.interfaces.abstract_view import AbstractView
from src.types.http_info import HTTPInfo


class Controller:

    def __init__(self, view: AbstractView,
                 update_period: int = 10,
                 traffic_history_span: int = 120,
                 traffic_limit: int = 10000):
        self.http_collector = BasicCollector(history_span=traffic_history_span)
        self.alert_manager = BasicAlertManager(traffic_limit=traffic_limit)
        self.update_period = update_period
        self.sniffer = ScapySniffer(receive_http_callback=lambda http_info: self._receive_http_callback(http_info))
        self.view = view
        self.stop_event = Event()
        self.traffic_history_span = traffic_history_span

    def _receive_http_callback(self, http_info: HTTPInfo):
        self.http_collector.collect_http_info(http_info)

    def start(self):
        self.sniffer.start()
        while not self.stop_event.is_set():
            time.sleep(self.update_period)
            alert_info: AlertInfo = self._manage_alert()
            self._update_view(alert_info)

    def _manage_alert(self) -> AlertInfo:
        traffic_over_span = self.http_collector.get_total_traffic_over_period(self.traffic_history_span)
        return self.alert_manager.get_alert_info(traffic_over_span)

    def _update_view(self, opt_alert_info: Optional[AlertInfo]):
        self.view.update_highest_hits(self.http_collector.get_highest_hits())
        self.view.update_traffic(self.http_collector.get_total_traffic())
        if opt_alert_info:
            self.view.update_alert_info(opt_alert_info)
        self.view.print_alert_info()
        self.http_collector.clear()

    def stop(self):
        self.stop_event.set()
        self.sniffer.stop()
