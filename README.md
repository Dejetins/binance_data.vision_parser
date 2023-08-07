# Binance Data Parser (Парсер данных Binance)
**This project is a parser designed to download, extract, and process trading pair data from Binance. The parser performs several key operations:**

**Этот проект представляет собой парсер, предназначенный для загрузки, извлечения и обработки данных торговых пар с сайта Binance. Парсер выполняет несколько ключевых операций:**

### Dependencies (Зависимости)
- pandas
- requests
- chardet
- BeautifulSoup
- zipfile
- concurrent.futures



1. Fetching Links and Downloading Data (Получение ссылок и загрузка данных)
File (Файл): `fetch_data.py`
Functionality (Функциональность): Downloads ZIP archives containing trading data for specified pairs (or all available pairs) and extracts the files. (Загружает ZIP-архивы, содержащие торговые данные для указанных пар (или всех доступных пар), и извлекает файлы.)


2. Extracting Trading Pair Links (Извлечение ссылок на торговые пары)
File (Файл): `get_links.py`
Functionality (Функциональность): Extracts trading pair links from an HTML list and saves them in JSON format. (Извлекает ссылки на торговые пары из HTML-списка и сохраняет их в формате JSON.)
3. Merging CSV Files (Объединение CSV-файлов)
File (Файл): `merge_data.py`
Functionality (Функциональность): Merges downloaded CSV files, saves them into a single CSV file, and then removes the original files. (Объединяет скачанные CSV-файлы, сохраняет их в один CSV-файл, а затем удаляет исходные файлы.)
4. Downloading and Extracting ZIP Files (Загрузка и извлечение ZIP-файлов)
File (Файл): `parse_data.py`
Functionality (Функциональность): Downloads and extracts ZIP file data for a given trading pair link and processes the data, including downloading and extracting ZIP files and merging the data. (Загружает и извлекает данные ZIP-файла для указанной торговой пары и обрабатывает данные, включая загрузку и извлечение ZIP-файлов и объединение данных.)
5. Data Transformation (Трансформация данных)
File (Файл): `transform_data.py`
Functionality (Функциональность): Reads and transforms data from the CSV file, including renaming columns, converting date formats, and sorting. (Читает и преобразует данные из CSV-файла, включая переименование столбцов, преобразование форматов даты и сортировку.)
6. User Interaction and Main Execution (Взаимодействие с пользователем и основное выполнение)
File (Файл): `main.py`
###Functionality (Функциональность):
Serves as the main entry point, allowing the user to select the language, and specify whether to download all available data or select specific trading pairs. (Является основной точкой входа, позволяя пользователю выбрать язык и указать, скачать ли все доступные данные или выбрать конкретные торговые пары.)
### How to Use (Как использовать)
The parser can be configured to download all files for trading pairs or specific ones separated by commas. At the beginning, the default language can be selected as well. (Парсер можно настроить на загрузку всех файлов для торговых пар или отдельных, разделенных запятыми. В начале можно также выбрать язык по умолчанию.)

### Conclusion (Заключение)
This parser offers a robust solution for gathering and processing trading data from Binance. The modular design allows for easy customization and extension as needed. (Этот парсер предлагает надежное решение для сбора и обработки торговых данных с Binance. Модульный дизайн позволяет легко настраивать и расширять его по мере необходимости.)
