from loader import dp, bot, admins


async def send_to_admin(dp):
    for admin in admins:
        await bot.send_message(admin, "Бот запущен")

