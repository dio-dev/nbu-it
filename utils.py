from random import shuffle
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from States import *
import asyncio
import os
from os.path import join, dirname
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import *
from aiohttp import BasicAuth
from dotenv import load_dotenv
from dbTools import *
from GoogleFinder import Google_finder
import re



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv("token")
BAD_CONTENT = ContentTypes.AUDIO
loop = asyncio.get_event_loop()
bot = Bot(TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


