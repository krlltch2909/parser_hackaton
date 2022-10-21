from aiogram import executor
from loader import dp
from handlers.user import *
from handlers import admin


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=admin.send_to_admin)
