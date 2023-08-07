# merge_data.py
import pandas as pd
import os
import chardet
from transform_data import read_and_transform_data
from datetime import datetime

def detect_encoding(file_path):
    """
    EN: Function to detect file encoding.
    RU: Функция для определения кодировки файла.

    :param file_path: path to the file / путь к файлу
    :return: file encoding / кодировка файла
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def merge_csv_files(pair_name):
    """
    EN: Function to merge downloaded csv files, save them into a single csv file, and then remove the original files.
    RU: Функция для объединения скачанных csv файлов, сохранения их в один csv файл, а затем удаления исходных файлов.

    :param pair_name: cryptocurrency trading pair name / имя торговой пары криптовалюты
    """
    data_folder = os.path.join('data/coin_prices', pair_name)
    files = os.listdir(data_folder)

    # EN: Read each file with auto detection of encoding
    # RU: Чтение каждого файла с автоматическим определением кодировки
    df = pd.concat([pd.read_csv(os.path.join(data_folder, file), header=None,
                                encoding=detect_encoding(os.path.join(data_folder, file))) for file in files],
                   ignore_index=True)

    output_folder = os.path.join('data/coin_prices', pair_name)

    # EN: If timeframe is embedded in the pair name (e.g., BTCUSDT_1m)
    # RU: Если таймфрейм встроен в имя пары (например, BTCUSDT_1m)
    pair_name_split = pair_name.split('_')
    if len(pair_name_split) > 1:
        pair_name, timeframe = pair_name_split
    else:
        # EN: replace with your own logic for determining the timeframe if it's not embedded in the pair name
        # RU: замените на свою логику определения таймфрейма, если он не встроен в имя пары
        timeframe = '5m'

    # EN: current date in year-month format
    # RU: текущая дата в формате год-месяц
    current_date = datetime.now().strftime('%Y-%m')
    output_file = os.path.join(output_folder, f'{pair_name}_{timeframe}_{current_date}_merged.csv')

    df.to_csv(output_file, index=False)

    # EN: Remove original files
    # RU: Удаление исходных файлов
    for file in files:
        file_path = os.path.join(data_folder, file)
        os.remove(file_path)

    # EN: Transform data
    # RU: Преобразование данных
    transformed_df = read_and_transform_data(output_file)


if __name__ == "__main__":
    pairs_directory = 'data/coin_prices'

    # EN: Get a list of all trading pairs
    # RU: Получение списка всех торговых пар
    trading_pairs = [dir_name for dir_name in os.listdir(pairs_directory) if
                     os.path.isdir(os.path.join(pairs_directory, dir_name))]

    for pair_name in trading_pairs:
        merge_csv_files(pair_name)
