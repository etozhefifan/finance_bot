import logging
from os import getenv

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from categories import Categories


load_dotenv()
API_TOKEN = getenv('API_TOKEN')
USER_ID = int(getenv('USER_ID'))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    import functools

    @functools.wraps(func)
    async def wrapper(message):
        if message['from']['id'] != USER_ID:
            return await message.reply('Аксесс денайд', reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm your new bot!", reply=False)


@dp.message_handler(commands=['categories'])
async def categories(message: types.Message):
    categories = Categories.get_all_categories()
    reply = (
        'Типы трат:'.join(
            [c.name+' ('+", ".join(c.aliases)+')' for c in categories]
            )
        )
    await message.answer(reply)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
