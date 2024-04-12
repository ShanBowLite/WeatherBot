from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, Location
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime

from keyboards.for_start import get_start_keyboard
from keyboards.for_city import get_city_keyboard
from keyboards.for_y_or_n import y_or_n
from geo.geocoding import get_cord, get_cord_ll
from geo.reverse_geocoding import get_city_name
from bd.bd import add_user, delete_user, search_user, change_city, check_user, get_city_link
from bd.user import User
from weather.weather_pars import get_forecast_day_str, get_forecast_week_str
from weather.weather import get_weather
from filters.chat_type import ChatTypeFilter 

#async def add_city(id:int,city_name:str):




router = Router()
router.message.filter(
    # Выставляем настройки фильтра на тип чата приватный
    ChatTypeFilter(chat_type=["private"])
) 

class Choosing_city(StatesGroup):
    choosing_city_name = State()
    check_city_name = State()

@router.message(Command("start")) 
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот помогающий узнать текущую погоду в твоём городе.",
         reply_markup=get_start_keyboard()
         )

@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=get_start_keyboard()
    )

@router.message(Command("city"))
@router.message(F.text.lower() == "указать город")
async def cmd_city(message: Message):
    await message.answer(
        "Выберите способ выбора города",
        reply_markup=get_city_keyboard()
    )


@router.message(Command("help"))
@router.message(F.text.lower() == "список доступных команд")
async def cmd_help(message: Message):
    await message.answer(
    f"В данный момент доступны команды:\n"
    f"/help - список действующих команд\n"
    f"/start - открыть главное меню\n"
    f"/weather - узнать погоду в своём городе\n"
    f"/weather_day - узнать прогноз погоды в своём городе на день\n"
    f"/weather_week - узнать прогноз погоды в своём городе на неделю\n"
    f"/city - указать город\n"
    f"/about_me - узнать обо мне\n",
    parse_mode="HTML"
    )


@router.message(Command("weather"))
@router.message(F.text.lower() == "узнать погоду")
async def cmd_weather(message: Message):
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Проверяем есть ли в нашей БД такой пользователь
    # Если есть, то сразу достаём все данные о нём.
    user = search_user(message.chat.id)
    if user == None:
        await message.answer(
        f"К сожалению я не знаю где вы находитесь\n"
        f"Пожалуйста, сначала укажите город",
        parse_mode="HTML",
        )
    else:
        res2 = 0
        city = user.city
        # Узнаём координаты города,т.к. api с температурой работает через координаты
        res, lat, lon = get_cord_ll(city)
        if res == 1:
            # Пытаемся узнать погоду
            res2, temp1, temp2 = get_weather(lat, lon)
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(
            text="Прогноз", url="https://yandex.ru/pogoda/nizhny-novgorod")
        )
        # Отправляем новое сообщение с с информацией о погоде
        if res2 == 1:
            await message.answer(
            f"Погода в городе {city} в {time_now} :\n"
            f"Температура {temp1}\u2103, ощущается как {temp2}\u2103\n",
            parse_mode="HTML",
            )
        else:
            await message.answer(
            f"К сожалению, в данный момент данные геомедиацентра недоступны. Попробуйте позже.",
            parse_mode="HTML",
            )

@router.message(Command("weather_day"))
@router.message(F.text.lower() == "узнать прогноз на день(тестируется)")
async def cmd_weather(message: Message):
    # Проверяем есть ли в нашей БД такой пользователь
    # Если есть, то сразу достаём все данные о нём.
    user = search_user(message.chat.id)
    if user == None:
        await message.answer(
        f"К сожалению я не знаю где вы находитесь\n"
        f"Пожалуйста, сначала укажите город",
        parse_mode="HTML",
        )
    else:
        city = user.city
        # Пытаемся достать из БД ссылку нужную ссылку на прогноз погоды по городу пользователя
        link = get_city_link(user.id)
        if link == None :
            await message.answer(
            f"К сожалению, в данный момент данные геомедиацентра недоступны. Попробуйте позже.",
            parse_mode="HTML",
            )
        else:
            # Пытаемся спарсить данные о погоде на этот день
            answer = get_forecast_day_str(link)
            if answer == None:
                await message.answer(
            f"К сожалению, в данный момент данные геомедиацентра недоступны. Попробуйте позже.",
            parse_mode="HTML",
            )
            else:
                await message.answer(
                answer+"\nИнформация взята с сайта https://www.gismeteo.ru", parse_mode="HTML",
                )
        
@router.message(Command("weather_week"))
@router.message(F.text.lower() == "узнать прогноз на неделю(тестируется)")
async def cmd_weather(message: Message):
    # Проверяем есть ли в нашей БД такой пользователь
    # Если есть, то сразу достаём все данные о нём.
    user = search_user(message.chat.id)
    if user == None:
        await message.answer(
        f"К сожалению я не знаю где вы находитесь\n"
        f"Пожалуйста, сначала укажите город",
        parse_mode="HTML",
        )
    else:
        city = user.city
        # Пытаемся достать из БД ссылку нужную ссылку на прогноз погоды по городу пользователя
        link = get_city_link(user.id)
        if link == None :
            await message.answer(
            f"К сожалению, в данный момент данные геомедиацентра недоступны. Попробуйте позже.",
            parse_mode="HTML",
            )
        else:
            # Пытаемся спарсить данные о погоде на неделю
            answer = get_forecast_week_str(link,city)
            if answer == None:
                await message.answer(
            f"К сожалению, в данный момент данные геомедиацентра недоступны. Попробуйте позже.",
            parse_mode="HTML",
            )
            else:
                await message.answer(
                answer+"\nИнформация взята с сайта https://www.gismeteo.ru", parse_mode="HTML",
                )

@router.message(F.text.lower() == "указать вручную")
async def message_ykaz_city(message: Message, state: FSMContext):
    await message.answer(
    f"Напишите название вашего города", 
    reply_markup=ReplyKeyboardRemove()
    )
    # Меняем состояние пользователя
    await state.set_state(Choosing_city.choosing_city_name)


@router.message(Choosing_city.choosing_city_name, F.text)
async def message_help(message: Message, state: FSMContext):
    # Пытаемся определить найдём ли координаты города по его названию
    res = get_cord(message.text)
    if res == 0:
        await message.answer("Извините, но я не смог найти такого города. "
        "Попробуйте снова. Или отмените выбор города ипользовав команду /cancel")
    else:
        # Раз координаты определили, то собираем инфу о пользователи
        user = User(message.chat.first_name, message.chat.last_name, message.chat.id, message.text)
        if search_user(message.chat.id) == None:
            # Если пользователь новый, то добавляем его в БД
            add_user(user)
        else:
            # Если пользователь не новый, то меняем его город в БД
            change_city(user)
        await message.answer("Отлично! Я запомнил в каком вы городе!",
        reply_markup=get_start_keyboard()
        )
        # Сбрасываем состояние пользователя
        await state.clear()

@router.message(F.location)
async def get_Location(message: Message,state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    # Пытаемся определить название города по координатам
    res, city_name = get_city_name(lat, lon)
    if res == 0:
        await message.answer("Извините, но я не смог найти такого города. "
        "Попробуйте снова. Или отмените выбор города ипользовав команду /cancel")
    else:
        # Раз город определили, то собираем инфу о пользователи
        user = User(message.chat.first_name, message.chat.last_name, message.chat.id, city_name)
        if check_user(message.chat.id):
             # Если пользователь не новый, то меняем его город в БД
            change_city(user)
        else:
            # Если пользователь новый, то добавляем его в БД
            add_user(user)
        await message.answer(
        f"Ваш город {city_name} ?",
        reply_markup=y_or_n()
        )
         # Меняем состояние пользователя
        await state.set_state(Choosing_city.check_city_name)

@router.message(Choosing_city.check_city_name, F.text.lower() == "да")
async def check_y(message: Message, state: FSMContext):
    await message.answer("Отлично! Я запомнил в каком вы городе!",
        reply_markup=get_start_keyboard()
        )
        # Сбрасываем состояние пользователя
    await state.clear()

@router.message(Choosing_city.check_city_name, F.text.lower() == "нет")
async def check_n(message: Message, state: FSMContext):
    delete_user(message.chat.id)
    await message.answer("Извините, но я не смог правильно определить город. "
        "Попробуйте снова использовав команду /city",
        reply_markup=get_start_keyboard()
        )
        # Сбрасываем состояние пользователя
    await state.clear()

@router.message(Command("about_me"))
@router.message(F.text.lower() == "узнать обо мне")
async def message_creaters(message: Message):
    await message.answer(
    f"Я нахожусь на стадии альфа-тестирования.\n"
    "Меня разрабатывают и тестируют студенты из группы 20-КТ.\n"
    "Меня создали на языке Python с помощью фреймворка aiogram 3.1.1\n"
    "Прогноз погоды берётся с сайта https://www.gismeteo.ru\n"
    "Также в разработке используются открытые api:\n"
    "1.Geocoding API - для определения названия города по коордлинатам и наоборот\n"
    "2.Current weather data API - для определения погоды по указанным координатам\n",
    parse_mode="HTML"
    )


@router.message(F.text)
async def message_help(message: Message):
    await message.answer(
    f"Извините, но я не знаю такой команды\n"
    f"Воспользуйтесь командой /help для того, чтобы узнать список известных мне команд.\n"
    f"Или командой /start для того, чтобы открыть главное меню",
    parse_mode="HTML"
    )
    