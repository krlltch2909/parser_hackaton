from aiogram import executor
from loader import dp
from handlers import *


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_to_admin)
