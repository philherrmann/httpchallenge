from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum


class AlertStatus(Enum):

    NO_ALERT = 0,
    OVER_THRESHOLD = 1,
    UNDER_THRESHOLD = 2


@dataclass(frozen=True)
class AlertInfo:

    status: AlertStatus
    traffic_value: int
    timestamp: float


class AbstractAlertManager(ABC):

    @abstractmethod
    def __init__(self, traffic_limit: int):
        """
        Instantiates an alert manager for a given traffic_limit (in bytes).
        Manages an internal state of type AlertStatus.
        :param traffic_limit: traffic (in bytes) used as alerting threshold
        """

    @abstractmethod
    def get_alert_info(self, traffic: int) -> Optional[AlertInfo]:
        """
        Returns an alert information in case a threshold is crossed ; plus manages alert status.
            - OVER_THRESHOLD if traffic just went over threshold (plus traffic value and timestamp)
            - UNDER_THRESHOLD if traffic just went over threshold (plus traffic value and timestamp)
        :param traffic: current amount of monitored traffic
        :return: alert info if threshold crossed, nothing otherwise
        """
