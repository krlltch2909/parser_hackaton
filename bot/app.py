from aiogram import executor
from loader import dp
from handlers.user import *
from handlers.on_start import on_start


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start)
