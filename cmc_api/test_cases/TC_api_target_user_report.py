import requests
import unittest
from cmc_api.common.api import Api
from cmc_api.common.exceptions import InvalidHasWapException


class MopCmcApiTest(unittest.TestCase):
    def setUp(self):
        self._api_host = 'vmlnx-k8s04.calix.local'
        self._api_port = '8080'
        self.org_id = '160090'
        self.payload = {"name": "All Subscribers", "desc": "Default filter"}

    @property
    def api_host(self):
        return self._api_host

    @property
    def api_port(self):
        return self._api_port

    @property
    def api_host_port(self):
        return self.api_host + ':' + self.api_port

    def test_haswap(self):
        url = 'http://' + self.api_host_port + Api.CMC_USER_REPORT + \
              '?org-id=160090&period=last-28d&attainable-rate=false&'
        payload = {"name": "All Subscribers", "desc": "Default filter"}
        has_wap_list = ['Y', 'N', None]

        print 'url:', url

        res = requests.post(url, json=payload)
        res_json = res.json()
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers

        for user_dic in res_json:
            self.assertIn(user_dic['hasWap'], has_wap_list, InvalidHasWapException().msg)

    def test_invalid_orgid(self):
        org_id_invalid = '160090aaa'
        url = 'http://' + self.api_host_port + Api.CMC_USER_REPORT + \
             '?org-id=' + org_id_invalid + '&period=last-28d&attainable-rate=false&'
        payload = {"name": "All Subscribers", "desc": "Default filter"}

        print 'url:', url

        res = requests.post(url, json=payload)
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        #print 'type(res.status_code):', type(res.status_code)
        self.assertEqual(400, res.status_code, 'STATUS_CODE should be 400')
        err_msg = 'Validation Error: error parameter [org-id], the input is [' + org_id_invalid \
                  + '], error: Invalid integer'
        self.assertIn(err_msg, res.text)

    def test_invalid_period(self):
        period_invalid = '888last-888e'
        url = 'http://' + self.api_host_port + Api.CMC_USER_REPORT + \
              '?org-id=' + self.org_id + '&period=' + period_invalid + '&attainable-rate=false&'

        print 'url:', url

        res = requests.post(url, json=self.payload)
        print 'STATUS_CODE:', res.status_code
        print 'HEADERS:', res.headers
        self.assertEqual(400, res.status_code, 'STATUS_CODE should be 400')
        #print 'res.text:', res.text
        err_msg = 'Validation Error: error parameter [period], the input is [' + period_invalid + \
                  '], error: Invalid option. The input can be: [last-28d, last-1m, last-2m, last-3m, ' \
                  'last-4m, last-5m, last-6m]'
        self.assertIn(err_msg, res.text)


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()