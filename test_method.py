from unittest import TestCase
import requests


class TestTornadoRequest(TestCase):
    base_url = 'http://localhost:8000'

    def test_index_post(self):
        url = self.base_url + '/'
        # 发起post请求，表单参数使用data来指定
        resp = requests.post(url, data={
            'name': ['ck', 'cxk'],
            'city': '山西'
        })
        print(resp.text)
