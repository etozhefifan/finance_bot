import psycopg2
from dotenv import load_dotenv
import os


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


def get_cursor():
    return cur
