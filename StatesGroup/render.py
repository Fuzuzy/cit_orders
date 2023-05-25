from aiogram.dispatcher.filters.state import State, StatesGroup
import easyocr
import re

class FSMRenderPhoto(StatesGroup):
    photo = State()

