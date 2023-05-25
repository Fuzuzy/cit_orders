from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import admin, client
from aiogram.dispatcher import FSMContext


async def on_startup(_):
    print("Бот вышел в онлайн")
    #sqlite_db.sql_start()


client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
