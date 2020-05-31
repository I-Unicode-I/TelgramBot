import os
from typing import Dict, List, Tuple

import sqlite3
import logging


# Connection to db with sqlite3.connection
conn = sqlite3.connect(os.path.join('../Telegram_bot7(StockBot)', 'Stock.db'))
# Create cursor for moving into db
cursor = conn.cursor()
# Create logging
logging.basicConfig(filename='ExecutDB.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(message)s')


def insert(table: str, column_values: Dict) -> None:
    """ Inserting data in tables """
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table}"
        f"({columns})"
        f"VALUES ({placeholders})",
        values
    )
    conn.commit()


def update(table: str, column: str, values: str, user_id: str) -> None:
    """ Update data in tables """
    val_id = [values, str(user_id)]
    cursor.execute(
        f"UPDATE {table} "
        f"SET {column}= ? "
        f"WHERE id= ?",
        val_id
    )
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """ Select all data from table """
    columns_joined = ', '.join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    """ Deleting data from table """
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    """ take cursor """
    return cursor


def _init_db():
    """Initialization DB"""
    with open('createdb.sql', 'r') as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Check, DB is initialization, if not -- initialization"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
