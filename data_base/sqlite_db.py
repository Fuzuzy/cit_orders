import sqlite3
from create_bot import dp, bot
import datetime


def sql_start():
    time = datetime.datetime.now().strftime('%m.%Y')
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    create_table_query = f'''
            CREATE TABLE IF NOT EXISTS '{time}' (
                message_text TEXT,
                message_date TEXT
            )
        '''
    cursor.execute(create_table_query)
    conn.commit()
