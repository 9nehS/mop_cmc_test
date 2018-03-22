import requests
import unittest
from cmc_api.common.api import Api


class MopCmcApiTest(unittest.TestCase):
    def setUp(self):
        self._api_host = 'vmlnx-k8s04.calix.local'
        self._api_port = '8080'
        self.org_id = '160090'
        self.pattern_connected_devices = '^0$|^[1-9]\d*$'

    @property
    def api_host(self):
        return self._api_host

    @property
    def api_port(self):
        return self._api_port

    @property
    def api_host_port(self):
        return self.api_host + ':' + self.api_port

    def test_last_28d(self):
        url = 'http://' + self.api_host_port + Api.CMC_CONNECTED_DEVICE_NUMBER_DISTRIBUTION + \
            '?org-id=' + self.org_id + '&period=last-28d&'
        key_list = ['0-5', '5-10', '10-15', '15-20', '20+']

        print 'url:', url

        res = requests.get(url)
        res_json = res.json()
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        # print res_json
        # print type(res_json)
        for dic in res_json:
            self.assertEqual(1, len(dic.keys()))
            for k, v in dic.items():
                self.assertIn(k, key_list)
                self.assertRegexpMatches(str(v), self.pattern_connected_devices)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()