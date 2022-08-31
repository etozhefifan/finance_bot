import database
from categories import Categories
from typing import NamedTuple, Optional
import re
import pytz
import datetime


class Message(NamedTuple):
    money_amount: int
    category_text: str


class Expense(NamedTuple):
    id: Optional[int]
    money_amount: int
    category_name: str


def add_expense(raw_message):
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    inserted_row_id = database.insert('expense', {
        'money_amount': parsed_message.money_amount,
        'created': _get_now_formatted(),
        'category_codename': category.codename,
        'raw_text': raw_message,
    })
    return Expense(
        id=None,
        money_amount=parsed_message.money_amount,
        category_name=category.name,
    )


def _parse_message(raw_message: str):
    regex_check = re.match(r'([\d ]+) (.*)', raw_message)
    if not regex_check:
        raise ValueError(
            """Некорректный формат сообщения.
            Пиши в формате: 200 еда"""
        )
    money_amount = regex_check.group(1).replace(' ', '')
    category_text = regex_check.group(2).strip().lower()
    return Message(money_amount=money_amount, category_text=category_text)


def get_statistic():
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cur = database.get_cursor()
    cur.execute('SELECT SUM(money_amount) '
                f'FROM expense WHERE created >= %s', [first_day_of_month])
    result = cur.fetchone()
    if not result[0]:
        return 'Ещё нет расходов в этом месяце'
    all_monthly_expenses = result[0] if result[0] else 0
    cur.execute(f'SELECT SUM(money_amount) FROM expense '
                f'WHERE created >= %s'
                f'AND category_codename IN (SELECT codename '
                f'FROM category WHERE is_basic_expense=TRUE)',
                [first_day_of_month])
    result = cur.fetchone()
    base_montly_expenses = result[0] if result[0] else 0
    return (f'Расходы за месяц:\n '
            f'всего — {all_monthly_expenses} \n'
            f'базовые — {base_montly_expenses}')


def last():
    cur = database.get_cursor()
    cur.execute(
        'SELECT E.id, E.money_amount, C.name '
        'FROM expense E LEFT JOIN category C '
        'ON C.codename=E.category_codename '
        'ORDER BY created DESC LIMIT 10'
    )
    rows = cur.fetchall()
    last_expenses = [Expense(id=row[0], money_amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_receipt(row_id):
    database.delete('expense', row_id)


def delete_receipts_for_month():
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cur = database.get_cursor()
    cur.execute(
        f'DELETE FROM expense WHERE created >= %s',
        [first_day_of_month]
    )

def _get_now_datetime():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    return now


def _get_now_formatted():
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")
