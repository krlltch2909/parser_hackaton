import os
import sys
import time
from timeloop import Timeloop
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.login import login


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS_IDS = os.getenv("ADMINS_IDS")

if BOT_TOKEN is None:
    sys.exit("Add BOT_TOKEN to .env file")
    
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

admins = []
if ADMINS_IDS is not None:    
    admins = ADMINS_IDS.split(",")
    admins = [admin for admin in admins if admin != ""]
timeloop = Timeloop()

django_start = False

while django_start is False:
    try:
        token = login()
        django_start = True
    except Exception:
        print("server is not active")
        time.sleep(3)

print("bot is ready")
