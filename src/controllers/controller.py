import time

from threading import Event
from typing import Optional
from src.alert_managers.basic_alert_manager import BasicAlertManager, AlertInfo
from src.interfaces.abstract_collector import HTTPInfo
from src.collectors.basic_collector import BasicCollector
from src.sniffers.scapy_sniffer import ScapySniffer
from src.interfaces.abstract_view import AbstractView


class Controller:

    def __init__(self,
                 view: AbstractView,
                 update_period: int = 10,
                 traffic_history_span: int = 120,
                 traffic_limit: int = 10000):
        """
        Controller for monitoring traffic and displaying information and alerts

        :param view: where the traffic / alerting information is displayed
        :param update_period: periodicity of traffic / alerting information update (in seconds, defaults to 10 seconds)
        :param traffic_history_span: duration during which traffic is monitored for alerting
               (in seconds, defaults to 2minutes)
        :param traffic_limit: traffic threshold used for alerting (in bytes, defaults to 10 thousand bytes - very low)
        """
        self.http_collector = BasicCollector(history_span=traffic_history_span)
        self.alert_manager = BasicAlertManager(traffic_limit=traffic_limit)
        self.update_period = update_period
        self.sniffer = ScapySniffer(receive_http_callback=lambda http_info: self._receive_http_callback(http_info))
        self.view = view
        self.stop_event = Event()
        self.traffic_history_span = traffic_history_span

    def start(self) -> None:
        """
        Starts sniffer, then periodically (period of self.update_period, defaults to 10 seconds) checks for alerts
        and updates the view with the traffic and alerting information.
        Stops when the stop event is set (cf. call to self.stop())
        """
        self.sniffer.start()
        while not self.stop_event.is_set():
            time.sleep(self.update_period)
            alert_info: AlertInfo = self._manage_alert()
            self._update_view(alert_info)
        self.sniffer.stop()

    def stop(self):
        """
        Stops the controller main start loop by setting the stop event.
        :return:
        """
        self.stop_event.set()

    def _receive_http_callback(self, http_info: HTTPInfo) -> None:
        """
        Callback for the HTTP traffic sniffer in case HTTP traffic is detected:
        collects the traffic if self.http_collector.
        :param http_info: detected HTTP traffic information
        """
        self.http_collector.collect_http_info(http_info)

    def _manage_alert(self) -> Optional[AlertInfo]:
        """
        Gets HTTP traffic over last self.traffic_history_span period (defaults to 2 minutes),
        relays this information to the alert manager and returns the alert information if any.
        :return: alert information if any, or None
        """
        traffic_over_span = self.http_collector.get_total_traffic_over_period(self.traffic_history_span)
        return self.alert_manager.get_alert_info(traffic_over_span)

    def _update_view(self, opt_alert_info: Optional[AlertInfo]) -> None:
        """
        Update the view with the (optional) alerting information and the traffic information (highest section hits).
        :param opt_alert_info: optional input alert information
        :return:
        """
        self.view.update_highest_hits(self.http_collector.get_highest_hits())
        if opt_alert_info:
            self.view.update_alert_info(opt_alert_info)
        self.view.print_alert_info()

