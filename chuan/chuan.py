import os.path
import time
from datetime import datetime
from random import random

import requests
import re
import logging

URL = 'https://chuan.us/'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../chuan.log',
                    filemode='w')


def log_it(func):
    def wrapper(*args, **kwargs):
        logging.info("Running function: %s" % func.__name__)
        result = func(*args, **kwargs)
        if not isinstance(result, Exception):
            logging.info("Result: %s" % result)
        else:
            logging.info(f"Fail to process {args}")
        return result
    return wrapper


def diff(func):
    def wrapper(*args, **kwargs):
        items = list(func(*args, **kwargs))
        count_now = len(list(items))
        now_date = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists('../last_count.txt'):
            with open('../last_count.txt', 'w', encoding='UTF-8') as f:

                f.write(f'{now_date}: {count_now}')
                return items

        with open('../last_count.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            last_line = lines[-1]
            count_last = int(re.search(r": (\d*)", last_line).group(1))

        if count_now != count_last:
            with open('../last_count.txt', 'a', encoding='UTF-8') as f:
                f.write(f'\n{now_date}: {count_now}')

            diff_count = count_now - count_last
            new_list = sorted(list(items), key=lambda x: x['date'], reverse=True)
            new_items = new_list[0:diff_count]
            return new_items

        else:
            try:
                import sys
                sys.exit()
            except SystemExit:
                logging.info('No change')

    return wrapper


@log_it
def scrape(url):
    try:
        response = requests.get(url)
        time.sleep(2 + 2 * random())
        return response

    except Exception as e:
        return e



@log_it
def convert_date(date_string) -> str:
    date_object = datetime.strptime(date_string, '%m/%d/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')

    return formatted_date


@log_it
def content(html_text):
    try:
        title = re.search(r"<h1.*?>(.*?)</h1>", html_text, re.MULTILINE).group(1)
        match1 = re.findall(r"<p>.*?</p>", html_text, re.MULTILINE)
        match2 = re.sub(r"<span.*?>|</span>|<p>", '', ''.join(match1), 0, re.MULTILINE)
        match3 = re.sub(r"</p>", '\n\n', match2, 0, re.MULTILINE)

        return {
            'title': title,
            'content': '## ' + title + '\n' + match3
        }

    except Exception as e:
        return e


@log_it
@diff
def link(html_text):
    try:
        matches = re.finditer(r"(https://chuan\.us/archives/\d*).*?(\d{1,2}/\d{1,2}/\d{4})", html_text, re.MULTILINE)

        for match in matches:
            item = {
                'link': match.group(1),
                'date': convert_date(match.group(2))
            }

            yield item

    except Exception as e:
        return e


@log_it
def save_md(file_name, string):
    try:
        with open(file_name, 'w', encoding='UTF-8') as f:
            f.write(string)
            return f'Successfully save file {file_name}'
    except Exception as e:
        return e
    finally:
        f.close()


def main():
    try:
        front_page = scrape(URL).text
        items = link(front_page)
        for item in items:
            url = item['link']
            detail = content(scrape(url).text)
            detail['title'] = re.sub(r"王川: ", item['date']+'_', detail['title'])
            save_md(file_name='sample/' + detail['title'] + '.md', string=detail['content'])

    except Exception:
        pass


if __name__ == '__main__':
    main()






