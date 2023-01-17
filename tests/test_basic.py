from .context import chuan

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    url = 'https://chuan.us/'
    front_page = open('tests/text/front_page.txt', 'r', encoding='UTF-8')
    detail_page = open('tests/text/detail_page.txt', 'r', encoding='UTF-8')
    md_text = open('tests/text/md_text.txt', 'r', encoding='UTF-8')

    def test_scrape(self):
        response = chuan.scrape(self.url)
        assert str(response) == '<Response [200]>'

    def test_link(self):
        items = list(chuan.link(self.front_page.read()))
        item = {'link': 'https://chuan.us/archives/690', 'date': '2021-10-26'}
        self.assertIn(item, items)
        self.assertTrue(len(items) >= 187)

    def test_content(self):
        detail = chuan.content(self.detail_page.read())
        assert detail['title'] and detail['content'] is not None

    def test_save_md(self):
        message = chuan.save_md('tests/text/md_text.md', self.md_text.read())
        self.assertEqual(message, 'Successfully save file tests/text/md_text.md')


if __name__ == '__main__':
    unittest.main()