import requests
import unittest
from cmc_api.common.api import Api
import cmc_api.utils


class MopCmcApiTest(unittest.TestCase):
    def setUp(self):
        self._api_host = 'vmlnx-k8s04.calix.local'
        self._api_port = '8080'
        self.org_id = '160090'
        self.pattern_number_of_devices = '^0$|^[1-9]\d*$'
        self.pattern_wifi_score = '^[1-5](\.\d)*$'

    @property
    def api_host(self):
        return self._api_host

    @property
    def api_port(self):
        return self._api_port

    @property
    def api_host_port(self):
        return self.api_host + ':' + self.api_port

    def test_one_month(self):
        url = 'http://' + self.api_host_port + Api.CMC_NUMBER_OF_DEVICES_AND_WIFISCORE_TREND_BY_MONTH + \
            '?org-id=160090&refresh=true&month=1'
        key_list = ['numberOfDevices', 'wifiScore']

        print 'url:', url

        res = requests.get(url)
        res_json = res.json()
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers

        self.assertEqual(2, len(res_json.keys()))
        for key in res_json.keys():
            self.assertIn(key, key_list)
        self.assertEqual(1, len(res_json['numberOfDevices']))
        self.assertEqual(1, len(res_json['wifiScore']))
        # print res_json['numberOfDevices'][0].keys()
        # print utils.last_month()
        self.assertEqual(cmc_api.utils.last_month(), res_json['numberOfDevices'][0].keys()[0])
        self.assertEqual(cmc_api.utils.last_month(), res_json['wifiScore'][0].keys()[0])
        self.assertRegexpMatches(str(res_json['numberOfDevices'][0][cmc_api.utils.last_month()]), self.pattern_number_of_devices)
        self.assertRegexpMatches(str(res_json['wifiScore'][0][cmc_api.utils.last_month()]), self.pattern_wifi_score)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()