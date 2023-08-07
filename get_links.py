# get_links.py
import json

html_list_file_m = 'data/html_list_m.txt'
html_list_file_d = 'data/html_list_d.txt'
trading_pairs_file_m = 'data/trading_pairs_m.json'
trading_pairs_file_d = 'data/trading_pairs_d.json'

def get_links(html_list_file, trading_pairs_file, period):
    """
    EN: Function to extract trading pair links from the HTML list and save them in JSON format.
    RU: Функция для извлечения ссылок на торговые пары из HTML списка и сохранения их в формате JSON.

    :param html_list_file: Path to the HTML list file / Путь к файлу HTML списка
    :param trading_pairs_file: Path to the JSON file to save trading pairs / Путь к файлу JSON для сохранения торговых пар
    :param period: Time period (monthly or daily) / Временной период (ежемесячно или ежедневно)
    """
    with open(html_list_file, 'r') as file:
        html_list = file.readlines()

    trading_pairs = {}

    # EN: Processing html_list and extracting USDT pair links
    # RU: Обработка html_list и извлечение ссылок на пары USDT
    for line in html_list:
        if 'USDT' in line:
            split_line = line.split('href="')
            link = split_line[1].split('">')[0]
            pair_name = split_line[1].split('">')[1].split('/')[0]
            if 'DOWN' in pair_name or 'UP' in pair_name or 'BULL' in pair_name or 'BEAR' in pair_name:
                continue  # EN: Skip pair containing "DOWN", "UP", "BULL", or "BEAR" / RU: Пропустить пару, содержащую "DOWN", "UP", "BULL" или "BEAR"

            # EN: Forming the link in the required format
            # RU: Формирование ссылки в требуемом формате
            formatted_link = f"https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/spot/{period}/klines/{pair_name}/5m/"

            trading_pairs[pair_name] = formatted_link

    # EN: Writing key-value pairs to trading_pairs_file in JSON format
    # RU: Запись пар ключ-значение в файл trading_pairs_file в формате JSON
    with open(trading_pairs_file, 'w') as file:
        json.dump(trading_pairs, file, indent=4)

if __name__ == "__main__":
    get_links(html_list_file_m, trading_pairs_file_m, 'monthly')
    get_links(html_list_file_d, trading_pairs_file_d, 'daily')
