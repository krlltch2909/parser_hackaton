import os
import time

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from utils.login import login

load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot)

django_start = False

while django_start is False:
    try:
        token = login()
        django_start = True
    except Exception:
        print("server is not active")
        time.sleep(3)

print("bot is ready")
