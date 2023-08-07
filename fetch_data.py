# fetch_data.py

import json
import datetime
from bs4 import BeautifulSoup
import requests
from parse_data import process_data


def fetch_all_file_links(pair_link):
    """
        EN: Function to fetch all ZIP file links for a given trading pair link.
        RU: Функция для получения всех ссылок на ZIP-файлы для данной торговой пары.

        :param pair_link: Link to the trading pair / Ссылка на торговую пару
        :return: List of file links / Список ссылок на файлы
        """
    page = requests.get(pair_link)
    xml_code = page.text
    soup = BeautifulSoup(xml_code, "xml")
    keys = soup.find_all("Key")
    file_links = []
    if keys:
        for key in keys:
            target_key = key.text
            if target_key.endswith('.zip'):
                file_link = "https://data.binance.vision/" + target_key
                file_links.append(file_link)
    return file_links

def fetch_data_for_pairs(trading_pairs_string):
    """
    EN: Function to fetch data for trading pairs either for all available pairs or for the specified pairs.
    RU: Функция для получения данных для торговых пар либо для всех доступных пар, либо для указанных пар.

    :param trading_pairs_string: String containing trading pairs or 'all' / Строка, содержащая торговые пары или 'all'
    """
    # EN: Set the current date to the first of the month
    # RU: Установить текущую дату на первое число месяца
    current_date = datetime.datetime.now().replace(day=1)

    # EN: Check if the user wants all trading pairs or specified ones
    # RU: Проверить, хочет ли пользователь все торговые пары или указанные
    if trading_pairs_string == 'all':
        with open('data/trading_pairs_m.json', 'r') as file:
            trading_pairs = json.load(file)
    else:
        trading_pairs_list = trading_pairs_string.split(',')
        trading_pairs = {pair_name: f"https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/spot/monthly/klines/{pair_name}/5m/" for pair_name in trading_pairs_list}
    # EN: Iterate through trading pairs and fetch file links
    # RU: Проход по торговым парам и получение ссылок на файлы
    for pair_name, pair_link in trading_pairs.items():
        pair_links = fetch_all_file_links(pair_link)

    for pair_name, pair_link in trading_pairs.items():
        pair_links = fetch_all_file_links(pair_link)

        # EN: Continue if there are no links
        # RU: Продолжить, если нет ссылок
        if not pair_links:
            continue
        # EN: Sort links by date
        # RU: Сортировка ссылок по дате
        pair_links.sort(key=lambda x: datetime.datetime.strptime(
            x.split('/')[-1].split('-')[2] + '-' + x.split('/')[-1].split('-')[3].replace('.zip', ''), '%Y-%m'))
        # EN: Get the last link and its date
        # RU: Получить последнюю ссылку и ее дату
        last_link = pair_links[-1] if pair_links else None
        last_link_date = datetime.datetime.strptime(
            last_link.split('/')[-1].split('-')[2] + '-' + last_link.split('/')[-1].split('-')[3].replace('.zip',
                                                                                                          ''),
            '%Y-%m') if last_link else None
        # EN: Check if the data is outdated and skip if it is
        # RU: Проверить, устарели ли данные, и пропустить, если это так
        if last_link and (current_date - last_link_date).days > 45:
            print(f"Data for {pair_name} is outdated. Skipping...")
            continue

        # EN: Create daily links of the current month except for today
        # RU: Создать ежедневные ссылки текущего месяца, кроме сегодняшнего дня
        base_daily_link = 'https://data.binance.vision/data/spot/daily/klines/'
        pair, timeframe = pair_name, '5m'
        daily_links = []
        for day in range(1, datetime.datetime.now().day - 1):  # subtracting 1 from the day
            date_part = f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{day:02d}"
            daily_link = f"{base_daily_link}{pair}/{timeframe}/{pair}-{timeframe}-{date_part}.zip"
            daily_links.append(daily_link)

        pair_links.extend(daily_links)

        # EN: Save links in temp_links.json file
        # RU: Сохранить ссылки в файле temp_links.json
        with open('data/temp_links.json', 'w') as file:
            json.dump({pair_name: pair_links}, file, indent=4)

        process_data(pair_name)

        with open('data/temp_links.json', 'w') as file:
            file.write("{}")


if __name__ == "__main__":
    trading_pairs_file_m = 'data/trading_pairs_m.json'

    fetch_data_for_pairs(trading_pairs_file_m)  # Fetching monthly data
