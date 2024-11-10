from aiogram.types import InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup

#
# старт:
#     регистрация (сначала warning)
#     настройки
#     узнать кто отписался сейчас
#
#
# настройки:
#     изменить данные
#     запустить/остановить бота
#     настроить частоту запросов
#     назад

keyboard_start = [
    [InlineKeyboardButton(text='Привязать инстаграм аккаунт', callback_data='registration')],
    [InlineKeyboardButton(text='Проверить аккаунт сейчас', callback_data='check_account')],
    [InlineKeyboardButton(text='Настройки', callback_data='Settings')],
]
# reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_start)



keyboard_settings = [
    [InlineKeyboardButton(text='Изменить профиль', callback_data='None')],
    [InlineKeyboardButton(text='Включить/Выключить бота', callback_data='None')],
    [InlineKeyboardButton(text='Изменить частоту запросов', callback_data='None')],
    [InlineKeyboardButton(text='Назад')],
]



keyboards = {'keyboard_start': keyboard_start,
             'keyboard_settings': keyboard_settings
             }


def get_keyboard(keyboard):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboards[keyboard])
    return reply_markup
