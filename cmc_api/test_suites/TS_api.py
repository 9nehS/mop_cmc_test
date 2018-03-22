# -*- coding: utf-8 -*-
import unittest
from cmc_api.test_cases.TC_api_connected_device_number_distribution import MopCmcApiTest as \
    API_CMC_CONNECTED_DEVICE_NUMBER_DISTRIBUTION
from cmc_api.test_cases.TC_api_number_of_devices_and_wifiscore_trend_by_month import MopCmcApiTest as \
    API_CMC_NUMBER_OF_DEVICES_AND_WIFISCORE_TREND_BY_MONTH
from cmc_api.test_cases.TC_api_target_user_report import MopCmcApiTest as API_CMC_USER_REPORT

if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [API_CMC_CONNECTED_DEVICE_NUMBER_DISTRIBUTION('test_last_28d'),
             API_CMC_NUMBER_OF_DEVICES_AND_WIFISCORE_TREND_BY_MONTH('test_one_month'),
             API_CMC_USER_REPORT('test_haswap'), API_CMC_USER_REPORT('test_invalid_orgid'),
             API_CMC_USER_REPORT('test_invalid_period')]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)