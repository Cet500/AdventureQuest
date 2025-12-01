from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import BASE_URL
from bot.keyboards import phone_request_kb

auth_router = Router()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_nickname = State()


@auth_router.message( Command( "start", "register" ) )
async def cmd_start(message: Message):
    await message.answer("Привет! Как тебя зовут?")
    await Registration.waiting_for_name.set()


@auth_router.message( state = Registration.waiting_for_name )
async def process_name( message: Message, state: FSMContext ):
    name = message.text.strip()
    if not name:
        name = message.from_user.full_name or "Игрок"
    await state.update_data( name = name )

    await message.answer(
        "Отправь, пожалуйста, свой номер телефона",
        reply_markup = phone_request_kb
    )
    await Registration.waiting_for_phone.set()


# @dp.message()
# async def register_user_player( message: types.Message ):
#     tg_id = message.from_user.id
#     name  = message.from_user.full_name  # Имя можно брать из Telegram
#     lang  = message.from_user.language_code
#
#     # 1. Регистрация пользователя
#     payload_user = {
#         "tg_id" : tg_id,
#         "name"  : name,
#         "lang"  : lang
#     }
#
#     print( payload_user )
#
#     resp = requests.post( f"{BASE_URL}/users", json = payload_user )
#
#     print( resp.json() )
#
#     if resp.status_code == 201:
#         user_id = resp.json()["id"]
#         await message.answer( "Вы зарегистрированы!" )
#
#     elif resp.status_code == 409:
#         # Получить существующего пользователя
#         user_data = requests.get( f"{BASE_URL}/users/tg/{tg_id}" ).json()
#         user_id = user_data["id"]
#         await message.answer( "Вы уже зарегистрированы." )
#
#     else:
#         await message.answer( "Ошибка регистрации." )
#         return
#
#     # 2. Создание игрока
#     payload_player = {
#         "nickname" : name,
#         "user_id"  : user_id
#     }
#
#     print( payload_player )
#
#     resp = requests.post( f"{BASE_URL}/players", json = payload_player )
#
#     print( resp.json() )
#
#     if resp.status_code == 201:
#         await message.answer( "Игрок создан, добро пожаловать в игру!" )
#
#     elif resp.status_code == 409:
#         await message.answer( "Вы уже игрок!" )
#
#     else:
#         await message.answer( "Ошибка при создании игрока." )