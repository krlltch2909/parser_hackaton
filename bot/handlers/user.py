import aiohttp
import asyncio
import os
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text
from loader import dp, bot, token
from keyboards.events_menu import events_menu


@dp.message_handler(Command("events"))
async def get_events_menu(message: Message):
    await message.delete()
    await message.answer("Выберите команду", reply_markup=events_menu)

@dp.message_handler(Text("Получить события"))
async def get_events_test(message: Message):
    await message.delete()
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": "Token " + token
        }
        async with session.get(url=os.getenv("API_BASE_URL") +"hackaton/", headers=headers) as response:
            data = await response.json(content_type=None)
            for event in data[:10]:
                await bot.send_message(message.from_user.id, text=event["title"])
