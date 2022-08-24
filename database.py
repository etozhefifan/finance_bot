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


def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                ID INT PRIMARY KEY NOT NULL,
                MONEY INT NOT NULL,
                CATEGORY TEXT NOT NULL,
                DATE TEXT);'''
                )


create_table()
conn.commit()


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