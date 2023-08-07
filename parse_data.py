# parse_data.py
from io import BytesIO
from zipfile import ZipFile
from zipfile import BadZipFile
import requests
import os
import json
from merge_data import merge_csv_files
from concurrent.futures import ThreadPoolExecutor


def download_and_extract_data(pair_name, file_link):
    """
        EN: Function to download and extract ZIP file data for a given trading pair link.
        RU: Функция для загрузки и извлечения данных ZIP-файла для данной торговой пары.

        :param pair_name: Trading pair name / Имя торговой пары
        :param file_link: Link to the ZIP file / Ссылка на ZIP-файл
        :return: Status of download (True, False, or None) / Статус загрузки (True, False или None)
        """
    # EN: Try downloading up to 5 times
    # RU: Попытка загрузки до 5 раз
    for attempt in range(5):
        try:
            response = requests.get(file_link)
            z = ZipFile(BytesIO(response.content))

            # EN: Create a directory if it doesn't exist
            # RU: Создать каталог, если он не существует
            os.makedirs(f"data/coin_prices/{pair_name}", exist_ok=True)

            # Download files
            z.extractall(path=f"data/coin_prices/{pair_name}")
            return True
        except BadZipFile:
            print(f"The file {file_link} is not a zip file")
            return None
        except Exception as e:
            print(f"Failed to download and extract file {file_link}. Error: {e}")
            if attempt < 2:  # if not last attempt
                print("Trying again...")
            else:
                return False



def process_data(pair_name):
    """
        EN: Function to process data for a given trading pair, download and extract ZIP files, and merge the data.
        RU: Функция обработки данных для данной торговой пары, загрузки и извлечения ZIP-файлов и объединения данных.

        :param pair_name: Trading pair name / Имя торговой пары
        """
    temp_links_file = 'data/temp_links.json'  # The file where you save links

    # Reading the temp_links.json file
    with open(temp_links_file, 'r') as file:
        all_links = json.load(file)

    if pair_name not in all_links:
        print(f"No file links found for {pair_name}.")
        return

    print(f"Downloading ticker data: {pair_name}")
    print(f"For {pair_name}, found {len(all_links[pair_name])} file links.")

    # EN: Creating an executor with № worker threads
    # RU: Создание исполнителя с рабочими потоками
    with ThreadPoolExecutor(max_workers=60) as executor:
        results = list(executor.map(lambda link: download_and_extract_data(pair_name, link), all_links[pair_name]))

    # EN: Count the number of successfully downloaded files
    # RU: Подсчет количества успешно загруженных файлов
    downloaded_files = results.count(True)
    failed_files = results.count(False)
    inaccessible_files = results.count(None)

    print(f"Downloaded {downloaded_files} out of {len(all_links[pair_name])} total files. {failed_files} files failed to download, {inaccessible_files} files were not accessible.")

    # EN: After downloading all the files, we call the merge function
    # RU: После загрузки всех файлов вызываем функцию объединения
    merge_csv_files(pair_name)
