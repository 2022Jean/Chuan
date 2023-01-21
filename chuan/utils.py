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
                    filemode='w',
                    encoding='UTF-8')


def log_print(message: str, *args, **kwargs) -> None:
    logging.info(message, *args, **kwargs)
    print(message, *args, **kwargs)


def truncate_strings(items: (list, dict, str), max_length: int) -> (list, dict, str):
    if isinstance(items, str):
        if len(items) > max_length:
            displayed_characters: str = items[:max_length]
            number_of_characters_not_displayed: int = len(items[max_length:])
            log_message = f"{displayed_characters}...{number_of_characters_not_displayed}" \
                          f" more characters not displayed..."
            return log_message
        else:
            return items
    elif isinstance(items, list):
        return [truncate_strings(x, max_length) for x in items]
    elif isinstance(items, dict):
        return {k: truncate_strings(v, max_length) for k, v in items.items()}
    else:
        return items


def log_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Running function: %s" % func.__name__)
        if func.__name__ == 'get_webpage':
            logging.info(f'Start scrape url: {args[0]}')

        result = func(*args, **kwargs)

        if func.__name__ != 'save_file' and result is None:
            logging.info(f'Return NOTHING from function {func.__name__}, end the program!!')
            exit()

        example_items = truncate_strings(result, 50)
        if isinstance(example_items, list):
            result_quantity: int = len(result)
            if result_quantity > 3:
                logging.info(f"Function {func.__name__} return a list consisting of {result_quantity} items, "
                             f"for example: {example_items[0:3]}")
            else:
                logging.info(f"Function {func.__name__} return a list consisting of {result_quantity} items, "
                             f"for example: {example_items}")
        else:
            logging.info(f'The example result function {func.__name__} returned: {example_items}')

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

    with open('download_history.txt', mode, encoding='UTF-8') as f:
        if mode == 'w':
            f.write('Below is download history: ')
        f.writelines(['\n' + message_item['message'] for message_item in message_items_timeline])


def clean_items(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> list[dict[str, str]]:
        items: list[dict[str, str]] = func(*args, **kwargs)
        items_quantity = len(items)

        if os.path.exists('download_history.txt'):
            with open('download_history.txt', 'r') as f:
                lines: list[str] = f.readlines()
                last_line: str = lines[-1]
                try:
                    date = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", last_line, re.MULTILINE)
                    log_print(f"Last download articles is in {date[0]} which wrote in {date[1]}")
                except AttributeError as attr_error:
                    log_print('AttributeError:', attr_error)
                except re.error as re_error:
                    log_print('RE error:', re_error)
                else:
                    items_quantity_old: int = len(lines) - 1
                    difference: int = items_quantity - items_quantity_old
                    if difference <= 0:
                        log_print('No change, end the program.')
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
