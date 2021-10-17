from typing import Callable
from threading import Event

import scapy.all as scapy_all
from scapy.layers.http import HTTPRequest

from src.interfaces.abstract_sniffer import AbstractSniffer
from src.types.http_info import HTTPInfo


class SnappySniffer(AbstractSniffer):

    def __init__(self, receive_http_callback: Callable[[HTTPInfo], None]):
        scapy_all.load_layer("http")
        self.stop_event = Event()
        self.receive_http_callback = receive_http_callback
        self.sniffer = scapy_all.AsyncSniffer(prn=self.manage_http_pkt, store=False, filter="tcp",
                                              stop_filter=lambda x: self.stop_event.is_set())

    def manage_http_pkt(self, pkt):
        if pkt.haslayer(HTTPRequest):

            content_length = 0
            try:
                #content_length = int.from_bytes(pkt.Content_Length, "big")
                #content_length2 = int.from_bytes(pkt.Content_Length, "big")
                if pkt.Content_Length is not None:
                    content_length = int(pkt.Content_Length.decode("utf-8"))
            except ValueError:
                logger.warn('Unable to decode HTTP Content-Length')
            print(f"pkt cl {pkt.Content_Length} type {type(pkt.Content_Length)} true cle {content_length}")
            http_info = HTTPInfo(host=pkt.Host, method=pkt.Method, path=pkt.Path,
                                 content_length=content_length)
            self.receive_http_callback(http_info)
            #print(pkt.summary())
            #print(pkt.show())
            '''
            curl http://google.fr//punkie//brewset/1000?q=1
                host = b'GET'
                host = b'google.fr'
                host = b'//punkie//brewset/1000?q=1'
            '''

    def start(self):
        print("start sniffing")
        self.sniffer.start()

    def stop(self):
        print("stop sniffing")
        self.stop_event.set()
