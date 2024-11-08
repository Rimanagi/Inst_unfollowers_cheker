import requests
import instaloader
import json
import os

from time import time
from datetime import date
from time import sleep
from dotenv import load_dotenv

ONE_DAY = 60 * 60 * 24

# Настройки
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PROXY = os.getenv('PROXY')

# Настройки прокси
proxies = {
    'http': PROXY,
}


def check_proxy(proxies):
    try:
        # Пробуем сделать запрос к Google через прокси
        response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("Прокси работает успешно!")
        else:
            print(f"Ошибка прокси: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при подключении через прокси: {e}")


def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(func.__name__, end - start)
        return result
    return wrapper


# Загрузка списка подписчиков
@function_timer
def get_followers_list(username):
    L = instaloader.Instaloader()
    L.context.timeout = 10
    L.context.proxy = proxies
    L.login(USERNAME, PASSWORD)

    profile = instaloader.Profile.from_username(L.context, username)
    return [follower.username for follower in profile.get_followers()]


# Сохранение списка в файл
def save_followers_list(followers, filename="followers.json"):
    with open(filename, 'w') as file:
        json.dump(followers, file)


# Загрузка списка из файла
def load_followers_list(filename="followers.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


# Сравнение списков
def find_unfollowers(old_list, new_list):
    return list(set(old_list) - (set(new_list)))


def send_telegram_notification(unfollower):
    message = f"https://www.instagram.com/{unfollower}/"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification:", response.text)


def main():
    while True:
        check_proxy(proxies)
        current_followers = get_followers_list(USERNAME)

        print('Got follower list')

        # Загружаем предыдущий список подписчиков
        previous_followers = load_followers_list()

        # Находим отписавшихся пользователей
        unfollowers = find_unfollowers(previous_followers, current_followers)

        # Отправляем уведомление, если есть отписавшиеся
        if unfollowers:
            for person in unfollowers:
                send_telegram_notification(person)

        # Сохраняем текущий список подписчиков
        save_followers_list(current_followers)

        print(f'{date.today()} has been checked')
        sleep(ONE_DAY)


if __name__ == "__main__":
    main()
