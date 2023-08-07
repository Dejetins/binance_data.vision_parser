# transform_data.py
import pandas as pd

def read_and_transform_data(file_path):
    """
    Читает и преобразует данные из файла.
    Reads and transforms data from the file.

    :param file_path: Путь к файлу.
                      The path to the file.
    :return: DataFrame с преобразованными данными.
             DataFrame with transformed data.
    """
    # Читаем файл CSV в DataFrame
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, header=None)

    # Удаляем первую строку из DataFrame
    # Remove the first row from the DataFrame
    df = df.iloc[1:]

    # Преобразуем первый столбец в формат даты и времени
    # Convert the first column to datetime format
    df[0] = pd.to_datetime(df[0], unit='ms')

    # Переименовываем столбцы
    # Rename the columns
    df.rename(columns={
        0: 'open_time',
        1: 'open',
        2: 'high',
        3: 'low',
        4: 'close',
        5: 'volume',
        7: 'quote_asset_volume',
        8: 'number_of_trades',
        9: 'taker_buy_base',
        10: 'taker_buy_quote',
    }, inplace=True)

    # Удаляем столбцы 'Close time' и 'Ignore'
    # Remove the 'Close time' and 'Ignore' columns
    df.drop(columns=[6, 11], inplace=True)

    # Сортируем DataFrame по столбцу 'open_time' в порядке убывания
    # Sort the DataFrame by the 'open_time' column in descending order
    df.sort_values(by='open_time', ascending=False, inplace=True)

    # Сохраняем DataFrame обратно в файл CSV
    # Save the DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    return df
