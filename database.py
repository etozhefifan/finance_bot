import psycopg2
from dotenv import load_dotenv
import os
import re


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
            dict_row[column]  = row[index]
        result.append(dict_row)
    return result



class Message():

    def __init__(self, money_amount, category):
        self.money_amount = money_amount
        self.category = category


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
    category = 