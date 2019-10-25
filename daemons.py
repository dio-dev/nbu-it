import asyncio
import datetime

from aiogram.types.inline_keyboard import *
from aiogram.types.reply_keyboard import *
from utils import bot

weekdays = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')


async def update_bd():
    pass


async def start_checker():
    counter = 0
    while True:
        await update_bd()

        counter += 1
        await asyncio.sleep(60)

