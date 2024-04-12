from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_keyboard() -> ReplyKeyboardBuilder:
    kb=ReplyKeyboardBuilder()
    kb.button(text="Указать город")
    kb.button(text="Узнать погоду")
    kb.button(text="Узнать прогноз на день(тестируется)")
    kb.button(text="Узнать прогноз на неделю(тестируется)")
    kb.button(text="Список доступных команд")
    kb.button(text="Узнать обо мне")
    kb.adjust(2,1,1)
    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Что вас интересует?"
        )
    