import logging
from os import getenv

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv
from categories import Categories
import finances


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
async def send_welcome(message):
    await message.reply("Hi! I'm your new bot!", reply=False)


@dp.message_handler(commands=['categories'])
@auth
async def categories(message):
    categories = Categories().get_all_categories()
    reply = (
        ''.join(
            [c.name + ' ('+", ".join(c.aliases)+')\n' for c in categories]
            )
        )
    await message.answer(reply)


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth
async def delete_receipt(message):
    row_id = int(message.text[4:])
    finances.delete_receipt(row_id)
    await message.answer('Удалил')


@dp.message_handler(commands=['statistic'])
@auth
async def statistics(message):
    await message.answer(finances.get_statistic())


@dp.message_handler(commands=['expenses'])
@auth
async def expenses(message):
    last_expenses = finances.last()
    if not last_expenses:
        await 'Нет расходов'

    last_expenses_rows = [
        f'{expense.money_amount} руб. потрачено на {expense.category_name}\n'
        for expense in last_expenses
    ]
    await message.answer(
        ''.join(last_expenses_rows)
        )


@dp.message_handler()
@auth
async def add_expense(message):
    try:
        receipt = finances.add_expense(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return
    answer_message = (
        f'Добавлен чек: {receipt.money_amount} руб. '
        f'в категорию: {receipt.category_name}\n'
        f'{finances.get_statistic()}'
    )
    await message.answer(answer_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
