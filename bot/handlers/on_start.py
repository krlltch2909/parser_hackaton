from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot
from .admin import send_to_admin


async def on_start(dp):
    await bot.set_my_commands(
        commands=[
            BotCommand("events", "Открыть меню мероприятий"),
            BotCommand("preferences", "Настроить интересы"),
            BotCommand("mailing", "Настройка рассылки мероприятий")
        ],
        scope=BotCommandScopeDefault()
    )
    await send_to_admin(dp)
    