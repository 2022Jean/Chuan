import logging
import re
from typing import List, Dict

import requests

from chuan.utils import convert_date

HEADERS = {
    'authority': 'chuan.us',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,applica'
              'tion/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_ga_3YPF1ZPFYX=GS1.1.1674193876.1.0.1674193876.0.0.0; _ga=GA1.1.781886078.1674193876; _tccl_visitor=84fb'
              'f8d2-66ed-575f-9bdd-69fa95e6ff92; _tccl_visit=84fbf8d2-66ed-575f-9bdd-69fa95e6ff92',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Sa'
                  'fari/537.36',
}

URL = 'https://chuan.us'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../chuan.log',
                    filemode='w')


def get_webpage(url: str) -> requests.Response:
    try:
        response = requests.get(url=url, timeout=10, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error_http:
        print("HTTP Error:", error_http)
    except requests.exceptions.ConnectionError as error_conn:
        print("Error Connecting:", error_conn)
    except requests.exceptions.Timeout as error_time:
        print("Timeout Error:", error_time)
    except requests.exceptions.RequestException as err:
        print("Something Else:", err)
    else:
        return response


def get_links(html_text: str) -> List[Dict[str, str]]:
    try:
        matches = re.finditer(r"(https://chuan\.us/archives/\d*).*?(\d{1,2}/\d{1,2}/\d{4})", html_text, re.MULTILINE)
        items = list()
        for match in matches:
            link = match.group(1)
            date = convert_date(match.group(2))
            item = {'link': link, 'date': date}
            items.append(item)
    except re.error as e:
        print(f"Regular expression error: {e}")
    else:
        return items


def get_article(html_text: str) -> Dict[str, str]:
    try:
        t1 = re.search(r"<h1.*?>(.*?)</h1>", html_text, re.MULTILINE).group(1)
        t2 = re.sub(r"/|&#8211;|&#8212;", '-', t1, 0)
        t3 = re.sub(r"&#8221;", '"', t2, 0)
        t4 = re.sub(r" ", '', t3, 0)
        t5 = re.sub(r"：", ':', t4, 0)

        title = t5

        c1 = re.findall(r"<p>.*?</p>", html_text, re.MULTILINE)
        c2 = re.sub(r"<span.*?>|</span>|<p>", '', ''.join(c1), 0, re.MULTILINE)
        c3 = re.sub(r"</p>", '\n\n', c2, 0, re.MULTILINE)
        # c4 = re.sub(r"&#8211;|&#8212;", '-', c3, 0, re.MULTILINE)
        # c5 = re.sub(r"&#8221;|&#8220;|&#8216;|”|“|&#8243", '"', c4, 0, re.MULTILINE)
        # c4 = re.sub(r"&#8217;", '', c5, 0, re.MULTILINE)

        content = c3

        content = '## ' + title + '\n' + content
        article = {'title': title, 'content': content}
    except re.error as e:
        print(f"Regular expression error: {e}")
    else:
        return article


def save_file(file_name: str, data: str) -> None:
    try:
        with open(file_name, 'w', encoding='UTF-8') as f:
            f.write(data)
    except FileExistsError as e:
        print(f"FileExistsError: {e}")
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except IOError as e:
        print(f"IOError: {e}")
    else:
        print(f"Successfully saved to {file_name}")



def main():
    pass


if __name__ == '__main__':
    main()