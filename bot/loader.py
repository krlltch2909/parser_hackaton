import os
import sys
import time
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.login import login
import logging
import logging.config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

logging.config.fileConfig(os.path.join(BASE_DIR, "logging.conf"), 
                          defaults={
                              "err_log_file": os.path.join(BASE_DIR, "logs/err/err.log"),
                              "out_log_file": os.path.join(BASE_DIR, "logs/out/out.log")
                          }, 
                          disable_existing_loggers=False)
logger = logging.getLogger(f"root.{__name__}")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS_IDS = os.getenv("ADMINS_IDS")

if BOT_TOKEN is None:
    logger.error("Can't find BOT_TOKEN env variable")
    sys.exit()
    
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

admins = []
if ADMINS_IDS is not None:    
    admins = ADMINS_IDS.split(",")
    admins = [admin for admin in admins if admin != ""]

django_start = False

while django_start is False:
    try:
        token = login()
        django_start = True
    except Exception:
        time.sleep(3)
