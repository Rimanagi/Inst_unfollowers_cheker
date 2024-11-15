from typing import Optional
from pathlib import Path

import asyncio
import aiosqlite
import json

DB_PATH = Path(__file__).parent / "../db/inst_followers.db"  # подстройте путь

async def create_database():
    async with aiosqlite.connect("inst_followers.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS inst_followers(
                tg_id INTEGER PRIMARY KEY,
                tg_username TEXT NOT NULL,
                inst_username TEXT NOT NULL,
                followers TEXT  -- Храним подписчиков как JSON-строку
            )
        """)
        # Сохраняем изменения
        await db.commit()
        print("Таблица создана!")


async def get_all_users_tg_usenames():
    async with aiosqlite.connect("inst_followers.db") as db:
        async with db.execute("SELECT tg_username FROM inst_followers") as cursor:
            res = await cursor.fetchall()
            print('ALL USERS')
            for r in res:
                print(*r)
            return res


async def get_followers(tg_id):
    async with aiosqlite.connect("inst_followers.db") as db:
        async with db.execute("SELECT followers FROM inst_followers WHERE tg_id = ?", (tg_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                followers_list = json.loads(row[0])  # Десериализуем JSON-строку в список
                print(f"Подписчики пользователя с tg_id {tg_id}: {followers_list}")
            else:
                print("Пользователь не найден")


async def add_user(tg_id, tg_username, inst_username):
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, существует ли пользователь с данным tg_id
        async with db.execute("SELECT 1 FROM inst_followers WHERE tg_id = ?", (tg_id,)) as cursor:
            user_exists = await cursor.fetchone()

        if user_exists:
            # Обновляем inst_username и сбрасываем поле followers, если пользователь существует
            await db.execute("""
                UPDATE inst_followers
                SET inst_username = ?, followers = NULL
                WHERE tg_id = ?
            """, (inst_username, tg_id))
            print(f"Обновлены данные для пользователя {tg_username}")
        else:
            # Вставляем нового пользователя, если он не существует
            await db.execute("""
                INSERT INTO inst_followers (tg_id, tg_username, inst_username, followers)
                VALUES (?, ?, ?, NULL)
            """, (tg_id, tg_username, inst_username))
            print(f"Пользователь {tg_username} добавлен в базу данных!")

        # Сохраняем изменения
        await db.commit()


async def update_followers(tg_id, followers):
    async with aiosqlite.connect("inst_followers.db") as db:
        await db.execute('''
            UPDATE inst_followers
            SET followers = ?
            WHERE tg_id = ?''',
            (followers, tg_id)
        )
    pass


async def update_user_info(tg_id, new_inst_username: Optional[str]=None, new_inst_password: Optional[str]=None):
    querry = ''
    value = []
    if new_inst_username:
        querry += 'inst_username=?'
        value.append(new_inst_username)
    if new_inst_password:
        querry += 'inst_password=?'
        value.append(new_inst_password)
    if not new_inst_password and not new_inst_username:
        print("Поле username и поле passwod не могут быть оба пустыми")
        return None

    async with aiosqlite.connect("inst_followers.db") as db:
        await db.execute(f"""
            UPDATE inst_followers
            SET {querry}
            WHERE tg_id=?""",
            (*value, tg_id)
        )
        await db.commit()

# asyncio.run(create_database())
# asyncio.run(add_user(11, 11, 'kek'))