from aiogram import types, Dispatcher
from create_bot import dp, bot
import re
import easyocr
from PIL import Image
import sqlite3
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import datetime
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Form(StatesGroup):
    entry1 = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Записать занос", "В разработке"]
    keyboard.add(*buttons)
    await message.reply("Цитозавр готов к бою!", reply_markup=keyboard)


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo(message: types.Message):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    reader = easyocr.Reader(['ru', 'en'])
    photo = message.photo[-1]
    photo_id = photo.file_id  # file id отправленного юзером
    photo_file = await bot.download_file_by_id(photo_id)

    with Image.open(photo_file) as image:
        result = reader.readtext(image, detail=0)

    string = ''
    for el in result:
        string += str(el)
        string += " "
    # print(string)
    articul = re.compile(r"\d{2}-\d{8}")  # форма для артикула
    match_articul = articul.findall(string)  # поиск артикула на фото
    if '00-00018386' in match_articul:
        match_articul.remove('00-00018386')
    elif '00-00019386' in match_articul:
        match_articul.remove('00-00019386')
    elif '00-00081781' in match_articul:
        match_articul.remove("00-00081781")
    string_art = ''.join(str(item) for item in match_articul)  # преобразование в строку
    # print(string)
    insert_data_query = '''
        INSERT INTO orders (articul, photo)
        VALUES (?, ?)
    '''
    data = (string_art, photo_id)
    cursor.execute(insert_data_query, data)
    conn.commit()
    await message.answer(f"Артикул: {string_art}")
    conn.close()


@dp.message_handler(Text(equals='Записать занос'))
async def add_money(message: types.Message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    markup.add(button)
    await Form.entry1.set()
    await message.reply("Введите сумму", reply_markup=markup)


@dp.callback_query_handler(Text('cancel'), state='*')
@dp.callback_query_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(call: types.callback_query, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await bot.send_message(call.message.chat.id, 'Отменено, для повторного ввода воспользуйтесь кнопкой заново')


@dp.message_handler(state=Form.entry1)
async def process_money(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['entry1'] = message.text
        name_quantity = message.text
        current_date = datetime.now()
        table_name = 'test'
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                money TEXT
            )
        '''
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(handle_photo, content_types=[types.ContentType.PHOTO])
    dp.register_message_handler(add_money, Text(equals='Записать занос'))
    dp.register_message_handler(process_money, state=Form.entry1)
    dp.register_message_handler(Text('cancel'), state='*')
