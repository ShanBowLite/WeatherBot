from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_city_keyboard() -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(text="Отправить геолокацию", request_location=True),
        types.KeyboardButton(text="Указать вручную")
    )
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие"
        )
