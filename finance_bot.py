import logging
from os import getenv

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = getenv('API_TOKEN')
USER_ID = int(getenv('USER_ID'))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    async def wrapper(message):
        if message['from']['id'] != USER_ID:
            return await message.reply('Аксесс денайд', reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm your new bot!")


if __name__ == "__main__":
    executor.start_polling(dp)
