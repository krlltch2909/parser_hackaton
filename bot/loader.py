import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot)
