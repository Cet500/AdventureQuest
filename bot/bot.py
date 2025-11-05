import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from config import TG_API_KEY, BASE_URL


bot = Bot( token = TG_API_KEY )
dp = Dispatcher()

logging.basicConfig( level = logging.INFO )


@dp.message()
async def echo(message: types.Message):
    response = requests.get( BASE_URL + '/' )

    await message.answer( response.text )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
