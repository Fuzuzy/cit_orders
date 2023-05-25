# import sqlite3 as sq
# from create_bot import dp, bot
#
# def sql_start():
#     global base, cur
#     base = sq.connect("orders.db")
#     cur = base.cursor()
#     if base:
#         print("База данных подключена")
#     base.execute('CREATE TABLE IF NOT EXISTS order(image TEXT, number TEXT, articul TEXT')