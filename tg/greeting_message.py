from aiogram import html
from aiogram.types import Message


def greeting_message(message: Message):
    message_text = f"""
Привет, **{html.quote(message.from_user.full_name)}**\!
Этот Бот отправляет уведомление, если кто\-то отписался от тебя в Инстаграме\*

\* ||Запрещенная организация в РФ||
"""
    return message_text

async def ask_login(message: Message, ):
    message_text = """
    Введите Ваш инстаграм
    (Ваш аккаунт должен быть публичным)"""
    return message_text

