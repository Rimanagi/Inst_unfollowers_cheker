from functools import wraps

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from greeting_message import greeting_message
from inline_keyboards import get_keyboard
from db import db_functions

router = Router()


class RegistrationStates(StatesGroup):
    waiting_for_username = State()


def register_handlers(dp, bot: Bot):
    def delete_previous_message(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            try:
                await bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass  # Обработка ошибок при удалении сообщения
            res = await func(message, *args, **kwargs)
            return res

        return wrapper

    @router.message(CommandStart())
    async def command_start_handler(message: Message) -> None:
        # Отправляем приветственное сообщение с клавиатурой
        await message.answer(
            greeting_message(message),
            parse_mode="MarkdownV2",
            reply_markup=get_keyboard("keyboard_start")
        )

    @router.callback_query(lambda callback: callback.data == "registration")
    async def prompt_inst_username(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text("Введите ваш Instagram username:")
        await state.set_state(RegistrationStates.waiting_for_username)

    @router.message(RegistrationStates.waiting_for_username, )
    @delete_previous_message
    async def add_inst_username_in_db(message: Message, state: FSMContext):
        inst_username = message.text
        await db_functions.add_user(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            inst_username=inst_username,
        )

        await state.clear()

    @router.callback_query()
    async def successful_registration_alert(callback: CallbackQuery, state: FSMContext):
        # callback.answer()
        # await command_start_handler(message)

    @router.message()
    async def delete_any_message(message: Message) -> None:
        await message.delete()

    dp.include_router(router)
