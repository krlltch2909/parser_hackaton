import asyncio
from jobs import send_new_events
from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot
from .admin import send_to_admin


async def start(dp):
    # Запускаем периодическую задачу для проверки новых мероприятий
    asyncio.create_task(send_new_events())
    await bot.set_my_commands(
        commands=[
            BotCommand("events", "Открыть меню мероприятий"),
            BotCommand("preferences", "Настроить интересы"),
            BotCommand("mailing", "Настройка рассылки мероприятий")
        ],
        scope=BotCommandScopeDefault()
    )
    await send_to_admin(dp)
