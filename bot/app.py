from aiogram import executor
from loader import dp
from jobs import *
from handlers.users.mailing_pref_handlers import *
from handlers.users.pref_menu_handlers import *
from handlers.users.user import *
from handlers.admin import *
from handlers.on_start import start
from handlers.on_shutdown import shutdown


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=start, 
                           on_shutdown=shutdown)
