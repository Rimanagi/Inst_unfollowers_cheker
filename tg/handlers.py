from functools import wraps
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from greeting_message import greeting_message
from inline_keyboards import get_keyboard

router = Router()


def register_handlers(dp, bot: Bot):
    def delete_previous_message(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            try:
                await bot.delete_message(message.chat.id, message.message_id - 1)
            except Exception:
                pass  # Обработка ошибок при удалении сообщения
            return await func(message, *args, **kwargs)

        return wrapper

    @router.message(CommandStart())
    async def command_start_handler(message: Message) -> None:
        # Отправляем приветственное сообщение с клавиатурой
        await message.answer(
            greeting_message(message),
            parse_mode="MarkdownV2",
            reply_markup=get_keyboard("keyboard_start")
        )

    @router.message()
    async def delete_any_message(message: Message) -> None:
        # Обработчик для других сообщений
        await message.delete()

    dp.include_router(router)
