import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import auth_router
from config import TG_API_KEY


logging.basicConfig( level = logging.INFO )

bot = Bot( token = TG_API_KEY )
dp = Dispatcher( storage = MemoryStorage() )


@dp.message( Command("check") )
async def cmd_start(message: Message):
    await message.answer("Я живой")


async def main():
    dp.include_router( auth_router )
    await dp.start_polling( bot )


if __name__ == '__main__':
    asyncio.run(main())
