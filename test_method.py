from unittest import TestCase
import requests


class TestTornadoRequest(TestCase):
    base_url = 'http://localhost:8000'

    def test_index_get(self):
        url = self.base_url + '/'
        # params表示查询参数
        resp = requests.get(url, params={
            'wd': 'ck',
            'title': '山西'
        })
        print(resp.text)

    def test_index_post(self):
        url = self.base_url + '/?wd=python'
        # 发起post请求，表单参数使用data来指定
        resp = requests.post(url, data={
            'name': ['ck', 'cxk'],
            'city': '山西'
        })
        print(resp.text)


class TestCookieRequest(TestCase):
    url = 'http://localhost:8000/cookie'

    def test_get(self):
        resp = requests.get(self.url)
        print(resp.text)

    def test_delete(self):
        resp = requests.delete(self.url, params={
            'name': 'token'
        })
        print(resp.text)


class TestOrderRequest(TestCase):
    url = 'http://localhost:8000/order/1/1'

    def test_get(self):
        resp = requests.get(self.url)
        print(resp.text)

    def test_post(self):
        resp = requests.post(self.url)
        print(resp.text)