import logging
import os.path
import re
from datetime import datetime
from functools import wraps

URL = 'https://chuan.us/'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='chuan.log',
                    filemode='w')


def log_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Running function: %s" % func.__name__)
        if func.__name__ == 'get_webpage':
            logging.info(f'Start scrape url: {args[0]}')

        result = func(*args, **kwargs)

        if result is None:
            logging.info(f'Return NOTHING from function {func.__name__}, end the program!!')
            exit()
        if func.__name__ == 'clean_items' or 'get_links' or 'wrapper':
            items_quantity = len(result)
            logging.info(f'Successfully get {items_quantity} links from function {func.__name__}')

        return result

    return wrapper


def write_download_message(mode: str, items: list[dict[str, str]]) -> None:
    date_today = datetime.now().strftime('%Y-%m-%d')
    download_message_items = list()
    for item in items:
        link, date = item['link'], item['date']
        message = f"{date_today} you download {link} wrote in {date}"
        message_items: dict[str, str] = {'date': date, 'message': message}
        download_message_items.append(message_items)
    message_items_timeline = sorted(download_message_items, key=lambda x: x['date'])

    with open('Chuan/download_history.txt', mode, encoding='UTF-8') as f:
        f.writelines([message_item['message'] for message_item in message_items_timeline])


def clean_items(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> list[dict[str, str]]:
        items: list[dict[str, str]] = func(*args, **kwargs)
        items_quantity = len(items)

        if os.path.exists('download_history.txt'):
            with open('download_history.txt', 'r') as f:
                lines: list[str] = f.readlines()
                last_line: str = lines[-1]
                date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", last_line, re.MULTILINE)
                if date.group(1) is not None:
                    items_quantity_old: int = len(lines)
                    difference: int = items_quantity - items_quantity_old
                    if difference <= 0:
                        exit()
                    items_timeline: list[dict[str, str]] = sorted(items, key=lambda x: x['date'], reverse=True)
                    new_items: list[dict[str, str]] = items_timeline[0:difference]

                    write_download_message(mode='a', items=new_items)

                    return new_items
        else:
            write_download_message(mode='w', items=items)

            return items

    return wrapper


def convert_date(date_string) -> str:
    date_object = datetime.strptime(date_string, '%m/%d/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')

    return formatted_date


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

if __name__ == '__main__':
    pass
