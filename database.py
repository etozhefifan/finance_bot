from typing import NamedTuple, Optional
import database
import psycopg2
from dotenv import load_dotenv
import os
import re

from categories import Categories


load_dotenv()
conn = psycopg2.connect(
                        dbname='expenses',
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        host='localhost',
                        port='5432',
                    )
cur = conn.cursor()


def fetchall(table, columns):
    columns_joined = ', '.join(columns)
    cur.execute(f'SELECT {columns_joined} FROM {table}')
    rows = cur.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def insert(table, column_values):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cur.executemany(
        f'INSERT INTO {table}'
        f'({columns})'
        f'VALUES ({placeholders})',
        values)

    conn.commit()


def delete(table, row_id):
    row_id = int(row_id)
    cur.execute(f'DELETE FROM {table} WHERE ID={row_id}')
    conn.commit()


class Message(NamedTuple):
    money_amount: int
    category: str


class Expense(NamedTuple):
    id: Optional[int]
    money_amount: int
    category: str


def _parse_message(message: str):
    regex_check = re.match(r'\d', message)
    if not regex_check:
        raise ValueError(
            """Некорректный формат сообщения.
            Пиши в формате: 200 еда"""
        )
    money_amount = regex_check[0]
    category = regex_check[1].strip().lower()
    return Message(money_amount=money_amount, category=category)


def add_receipt(raw_message):
    parsed_message = _parse_message(raw_message)
    category = Categories.get_category(parsed_message.category)
    inserted_row_id = database.insert('expense', {
        'money_amount': parsed_message.money_amount,
        'created': _get_now_formatted(),
        'category_codename': category.codename,
        'raw_text': raw_message,
    })
    return Expense(
        id=None,
        money_amount=parsed_message.money_amount,
        category=category.name,
    )
