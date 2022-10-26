import os
import time
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.login import login

load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
admins = os.getenv("ADMINS_ID").split(",")
admins = [admin for admin in admins if admin != ""]
django_start = False

while django_start is False:
    try:
        token = login()
        django_start = True
    except Exception:
        print("server is not active")
        time.sleep(3)

print("bot is ready")
