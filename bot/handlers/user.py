import aiohttp
import os
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text
from loader import dp, bot, token
from keyboards.default.events_menu import events_menu


@dp.message_handler(Command("start"))
async def show_start_menu(message: Message):
    await message.answer("Добро пожаловать. Веберите команду /events" \
        " для начала работы с мероприятиями\nВы также можете выбрать команду /preferences" \
        " для уточнения интересующих мероприятий")


@dp.message_handler(Command("events"))
async def show_menu(message: Message):
    await message.answer("Выберите интересующий способ получения мероприятий", 
                        reply_markup=events_menu)


@dp.message_handler(Text("Все события"))
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
