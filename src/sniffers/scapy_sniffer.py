from typing import Callable, Optional
from threading import Event

import scapy.all as scapy_all
from scapy.layers.http import HTTPRequest

from src.interfaces.abstract_sniffer import AbstractSniffer
from src.interfaces.abstract_collector import HTTPInfo

from logging import getLogger

logger = getLogger("ScapySniffer")


class ScapySniffer(AbstractSniffer):

    def __init__(self, receive_http_callback: Callable[[HTTPInfo], None]):
        scapy_all.load_layer("http")
        self.stop_event = Event()
        self.receive_http_callback = receive_http_callback
        self.sniffer = scapy_all.AsyncSniffer(prn=self.manage_http_pkt, store=False, filter="tcp",
                                              stop_filter=lambda x: self.stop_event.is_set())

    @staticmethod
    def parse_packet(pkt) -> Optional[HTTPInfo]:
        try:
            if pkt.Content_Length is not None and pkt.Host is not None \
                    and pkt.Method is not None and pkt.Path is not None:
                content_length = int(pkt.Content_Length.decode("utf-8"))
                host = pkt.Host.decode('utf-8')
                method = pkt.Method.decode('utf-8')
                path = pkt.Path.decode('utf-8')
                return HTTPInfo(content_length=content_length, host=host,
                                method=method, path=path)
            else:
                return None
        except (ValueError, UnicodeDecodeError):
            logger.warning('Unable to decode packet')
        return None

    def manage_http_pkt(self, pkt) -> None:
        if pkt.haslayer(HTTPRequest):
            http_info = ScapySniffer.parse_packet(pkt)
            if http_info is not None:
                self.receive_http_callback(http_info)

    def start(self) -> None:
        self.sniffer.start()

    def stop(self) -> None:
        self.stop_event.set()
