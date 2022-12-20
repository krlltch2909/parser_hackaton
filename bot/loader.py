import os
import sys
import time
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from login import get_token
import logging
import logging.config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# Создаем папки для логов    
if not os.path.exists(os.path.join(BASE_DIR, "logs/err")) and \
    not os.path.exists(os.path.join(BASE_DIR, "logs/out")):
        os.mkdir(os.path.join(BASE_DIR, "logs/err"))
        os.mkdir(os.path.join(BASE_DIR, "logs/out"))

# Конфигурация логгера
logging.config.fileConfig(os.path.join(BASE_DIR, "logging.conf"), 
                          defaults={
                              "err_log_file": os.path.join(BASE_DIR, "logs/err/err.log"),
                              "out_log_file": os.path.join(BASE_DIR, "logs/out/out.log")
                          }, 
                          disable_existing_loggers=False)
logger = logging.getLogger(f"root.{__name__}")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    logger.error("Can't find BOT_TOKEN env variable")
    sys.exit()
    
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

ADMINS_IDS = os.getenv("ADMINS_IDS")
admins = []
if ADMINS_IDS is not None:    
    admins = ADMINS_IDS.split(",")
    admins = [admin for admin in admins if admin != ""]

django_start = False

while django_start is False:
    try:
        token = get_token()
        django_start = True
    except Exception:
        time.sleep(3)
