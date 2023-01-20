import requests

from chuan import core

import unittest


class CoreTestCase(unittest.TestCase):
    url1 = 'https://chuan.us'
    url2 = 'https://chuan.us/archives/877'

    def test_get_webpage(self):
        response1 = requests.get(self.url1)
        response2 = requests.get(self.url2)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_get_links(self):
        pass

    def test_get_article(self):
        pass