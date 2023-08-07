import json
from fetch_data import fetch_data_for_pairs

# EN: Messages for English and Russian languages
# RU: Сообщения на английском и русском языках
MESSAGES = {
    "en": {
        "choice": "Enter 'all' to download all available data or 'select' to choose trading pairs: ",
        "pairs": "Enter the trading pair names separated by a comma (e.g., BTCUSDT,ETHUSDT): ",
        "wrong_choice": "Incorrect choice. Please restart the program."
    },
    "ru": {
        "choice": "Введите 'all' для скачивания всех доступных данных или 'select' для выбора торговых пар: ",
        "pairs": "Введите названия торговых пар через запятую (например, BTCUSDT,ETHUSDT): ",
        "wrong_choice": "Неверный выбор. Пожалуйста, запустите программу заново."
    }
}

def save_language_choice(language):
    with open("language_choice.json", "w") as file:
        json.dump({"language": language}, file)

def load_language_choice():
    try:
        with open("language_choice.json", "r") as file:
            return json.load(file)["language"]
    except:
        return None

if __name__ == "__main__":
    language = load_language_choice()

    if not language:
        language = input("Choose language (en/ru): ").strip().lower()
        save_language_choice(language)

    msgs = MESSAGES.get(language, MESSAGES["en"])

    choice = input(msgs["choice"]).strip().lower()

    if choice == 'all':
        fetch_data_for_pairs('all')
    elif choice == 'select':
        trading_pairs = input(msgs["pairs"])
        fetch_data_for_pairs(trading_pairs)
    else:
        print(msgs["wrong_choice"])
