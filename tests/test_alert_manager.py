from unittest import TestCase
from typing import Optional
from src.alert_managers.basic_alert_manager import BasicAlertManager, AlertInfo, AlertStatus


class TestAlertManager(TestCase):

    def setUp(self):
        self.traffic_limit = 1000
        self.alert_manager = BasicAlertManager(traffic_limit=self.traffic_limit)

    def test_alert_manager_stays_under_threshold(self):
        '''
        Test case: emit traffic but under threshold
        Test output: no alert emitted
        '''
        total_traffic = 0
        added_traffic = 100
        while total_traffic < self.traffic_limit:
            total_traffic += added_traffic
            alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(added_traffic)
            self.assertIsNone(alert_info)

    def test_alert_manager_goes_over_then_under_threshold(self):
        '''
        Test case: emit traffic over threshold, check "over threshold" alert is emitted,
                   then traffic goes under threshold, check recovery alert is emitted,
                   then traffic stays under threshold, no alert emitted.
        '''

        # traffic goes up but stays under threshold
        total_traffic = 0
        added_traffic = 100
        while total_traffic < self.traffic_limit:
            total_traffic += added_traffic
            alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(total_traffic)
            self.assertIsNone(alert_info)

        # traffic goes over threshold -> alert should be emitted
        total_traffic += added_traffic
        self.assertGreater(total_traffic, self.traffic_limit)
        alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(total_traffic)
        self.assertIsNotNone(alert_info)
        self.assertEqual(alert_info.status, AlertStatus.OVER_THRESHOLD)

        # traffic stays over threshold -> no alert
        alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(total_traffic)
        self.assertIsNone(alert_info)

        # traffic goes under threshold (equal to threshold here) -> recovery emitted
        total_traffic -= added_traffic
        self.assertLessEqual(total_traffic, self.traffic_limit)
        alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(total_traffic)
        self.assertIsNotNone(alert_info)
        self.assertEqual(alert_info.status, AlertStatus.UNDER_THRESHOLD)

        # traffic stays under threshold -> no alert
        alert_info: Optional[AlertInfo] = self.alert_manager.get_alert_info(total_traffic)
        self.assertIsNone(alert_info)