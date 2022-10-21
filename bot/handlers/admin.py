import os
from loader import dp, bot


async def send_to_admin(dp):
    await bot.send_message(os.getenv("ADMIN_ID"), "Бот запущен")
