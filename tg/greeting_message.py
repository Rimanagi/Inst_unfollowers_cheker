import html
from aiogram import html
from aiogram.types import Message

MarkdownV2_symbols = {
    '*': '\*',
    '_': '\_',
    '[': '\[',
    ']': '\]',
    '(': '\(',
    ')': '\)',
    '~': '\~',
    '\\': '\\\\',
    '.': '\.'}

def greeting_message(message: Message):
    # user_name = message.from_user.first_name
    # for char in user_name:
    #     user_name = user_name.replace(char, MarkdownV2_symbols[char])
    # , **{user_name}**
    message_text = f"""
Привет\!
Этот Бот отправляет уведомление, если кто\-то отписался от тебя в Инстаграме\*

\* ||Запрещенная организация в РФ||
"""
    return message_text


async def ask_login(message: Message, ):
    message_text = """
    Введите Ваш инстаграм
    (Ваш аккаунт должен быть публичным)"""
    return message_text

