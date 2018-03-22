import requests
import unittest
from cmc_api.common.api import Api
from cmc_api.common.exceptions import InvalidUserCountException
from cmc_api.common.exceptions import InvalidHasWapException


class MopCmcApiTest(unittest.TestCase):
    def setUp(self):
        self._api_host = 'vmlnx-k8s04.calix.local'
        self._api_port = '8080'

    @property
    def api_host(self):
        return self._api_host

    @property
    def api_port(self):
        return self._api_port

    @property
    def api_host_port(self):
        return self.api_host + ':' + self.api_port

    def test_number_of_devices_and_wifiscore_trend_by_month(self):
        url = 'http://' + self.api_host_port + \
              Api.CMC_NUMBER_OF_DEVICES_AND_WIFISCORE_TREND_BY_MONTH + '?org-id=160090&refresh=true&month=6'
        print 'url:', url
        res = requests.get(url)
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        print res.json()

    def test_target_user_counts(self):
        url = 'http://' + self.api_host_port + Api.CMC_TARGET_USER_COUNTS + \
              '?period=last-28d&org-id=160090&refresh=true'
        payload = {"name":"All Subscribers","desc":"Default filter"}
        pattern = '^\d+$'

        print 'url:', url

        res = requests.post(url, json=payload)
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        res_json = res.json()

        self.assertRegexpMatches(str(res_json["userCount"]), pattern, InvalidUserCountException().msg)

    def test_target_user_report(self):
        url = 'http://' + self.api_host_port + Api.CMC_USER_REPORT + \
              '?org-id=160090&period=last-28d&attainable-rate=false&'
        payload = {"name": "All Subscribers", "desc": "Default filter"}
        has_wap_list = ['Y', 'N', None]

        print 'url:', url

        res = requests.post(url, json=payload)
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        res_json = res.json()

        for user_dic in res_json:
            self.assertIn(user_dic['hasWap'], has_wap_list, InvalidHasWapException().msg)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()