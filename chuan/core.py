import re
from typing import List, Dict

import requests

from chuan.utils import convert_date, HEADERS, log_it, clean_items, log_print

URL = 'https://chuan.us'


@log_it
def get_webpage(url: str) -> requests.Response:
    try:
        response = requests.get(url=url, timeout=10, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error_http:
        log_print("HTTP Error:", error_http)
    except requests.exceptions.ConnectionError as error_conn:
        log_print("Error Connecting:", error_conn)
    except requests.exceptions.Timeout as error_time:
        log_print("Timeout Error:", error_time)
    except requests.exceptions.RequestException as err:
        log_print("Something Else:", err)
    else:
        return response


@log_it
@clean_items
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
        log_print(f"Regular expression error: {e}")
    else:
        return items


@log_it
def get_article(html_text: str) -> Dict[str, str]:
    try:
        t1 = re.search(r"<h1.*?>(.*?)</h1>", html_text, re.MULTILINE).group(1)
        t2 = re.sub(r"/|&#8211;|&#8212;", '-', t1, 0)
        t3 = re.sub(r"：|:|王川：|王川:| |\?|\*|，|。|\u3000|&#8221;|“|”|\"|'|？", '', t2, 0)
        t4 = re.sub(r"（", '(', t3, 0)
        t5 = re.sub(r"）", ')', t4, 0)

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
        log_print(f"Regular expression error: {e}")
    else:
        return article


def save_file(file_name: str, data: str) -> None:
    try:
        with open(file_name, 'w', encoding='UTF-8') as f:
            f.write(data)
    except FileExistsError as e:
        log_print(f"FileExistsError: {e}")
    except PermissionError as e:
        log_print(f"PermissionError: {e}")
    except IOError as e:
        log_print(f"IOError: {e}")
    else:
        log_print(f"Successfully saved to {file_name}")


@log_it
def main():
    front_page: str = get_webpage(URL).text
    link_list: list[dict[str, str]] = get_links(front_page)
    for link_item in link_list:
        url: str = link_item['link']
        article_page: str = get_webpage(url).text
        article: dict = get_article(article_page)
        file_name: str = "../example_files/" + link_item['date'] + '_' + article['title'] + '.md'
        save_file(file_name, article['content'])


if __name__ == '__main__':
    main()
