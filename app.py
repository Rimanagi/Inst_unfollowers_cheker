import asyncio
import os
from time import sleep

from dotenv import load_dotenv
from instagrapi import Client

ONE_DAY = 60 * 60 * 24

# Настройки
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
PROXY = os.getenv('PROXY')


cl = Client()
cl.login(USERNAME, PASSWORD)
async def main():
    while True:
        # todo настроить проксю
        # cl.set_proxy() =
        inst_username = cl.user_id_from_username('dunken_augen')
        # todo: Пример возрата метода user_follower | возвращать только его ID и username (id на случай если человек поменяет никнейм)

        # '65359113616': UserShort(pk='65359113616', username='rapeg65151',
        # full_name='kcdo', profile_pic_url=Url('тут ссылка'), profile_pic_url_hd=None, is_private=None),
        #
        user_followers = cl.user_followers(inst_username)
        print(user_followers)
        await asyncio.sleep(ONE_DAY)


if __name__ == "__main__":
    main()
