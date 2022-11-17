from aiogram import executor
from loader import dp, timeloop
from jobs import *
from handlers.users.user import *
from handlers.users.mailing_pref_handlers import *
from handlers.users.pref_menu_handlers import *
from handlers.admin import *
from handlers.on_start import on_start


if __name__ == "__main__":
    # Запускаем периодическую задачу для проверки новых мероприятий
    timeloop.start(block=False)
    executor.start_polling(dp, on_startup=on_start)
