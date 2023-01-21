import unittest

from chuan import utils


class UtilsTestCase(unittest.TestCase):

    def test_truncate_strings(self):
        long_list: list = [
            'Lorem ipsum dolor sit amet',
            [
                'Lorem ipsum dolor sit amet',
                {
                    'key1': 'Lorem ipsum dolor sit amet',
                    'key2': 'Lorem ipsum dolor sit amet'
                }
            ]
        ]
        short_list: list = [
            'Lorem ipsum dolor sit...5 more characters not displayed...',
            [
                'Lorem ipsum dolor sit...5 more characters not displayed...',
                {
                    'key1': 'Lorem ipsum dolor sit...5 more characters not displayed...',
                    'key2': 'Lorem ipsum dolor sit...5 more characters not displayed...'
                }
            ]
        ]
        self.assertEqual(short_list, utils.truncate_strings(long_list, 21))

    def test_convert_date(self):
        date = '01/21/2023'
        self.assertEqual('2023-01-21', utils.convert_date(date))


if __name__ == '__main__':
    unittest.main()
