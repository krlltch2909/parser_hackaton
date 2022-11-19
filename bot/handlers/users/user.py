import os
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.default.events_menu import events_menu
from keyboards.inline.events_list_keyboard import get_events_list_keyboard
from utils.create_event_message import create_event_messsage
from utils.get_indexes import get_indexes
from utils.database import user_preferences_collection
from utils.parser_api import get_events, get_events_by_preferences
from models.Event import Event


PAGE_SIZE = os.getenv("EVENTS_PAGE_SISE")
PAGE_SIZE = int(PAGE_SIZE) if PAGE_SIZE is not None else 5


@dp.message_handler(Command("start"))
async def show_start_menu(message: types.Message):
    await message.answer("Добро пожаловать!\nВыберите команду /events" \
        " для начала работы с мероприятиями.\nКоманда /preferences" \
        " позволит вам выбрать категории для отображения инетересующих вас мероприятий." \
        "\nС помощью команды /mailing вы сможете настроить режим рассылки информации о мероприятиях.")


@dp.message_handler(Command("events"))
async def show_events_menu(message: types.Message):
    await message.answer("Выберите интересующий способ получения мероприятий",
                         reply_markup=events_menu)


@dp.message_handler(lambda message: message.text and message.text\
    in ["Все события", "Интересующие события"])
async def get_all_events(message: types.Message, state: FSMContext):
    events: list[Event] = []

    if message.text == "Все события":
        events.extend(await get_events())
    elif message.text == "Интересующие события":
        user_preferences = await user_preferences_collection.find_one({"_id": message.from_user.id})
        if user_preferences is not None:
            events_types = user_preferences["events_types"]
            tags = user_preferences["tags"]

            if len(events_types) == 0 and len(tags) == 0:
                await bot.send_message(message.from_user.id, text="Вы не указали ваши предпочтения.\n"\
                    "Воспользуйтесь командой /preferences.")
                return
            else:
                events.extend(await get_events_by_preferences(events_types, tags))
        else:
            await bot.send_message(message.from_user.id, text="Для того, чтобы воспользоваться данной" \
                " функцией вы должны указать свои предпочтения, " \
                "воспользовавшись командой /preferences.")
            return

    # Сохраняем ивенты в состояние
    await state.update_data(events=events)
    # Количество событий в одном сообщении
    await state.update_data(page_size=PAGE_SIZE)
    await state.update_data(current_page=1)

    await message.delete()
    result_message = ""
    data = await state.get_data()
    page_size = int(data.get("page_size"))
    for raw_event in data.get("events")[:page_size]:
        result_message += create_event_messsage(raw_event)
        result_message += "---------------------------\n\n"
    await bot.send_message(message.from_user.id,
                           result_message,
                           parse_mode="HTML",
                           disable_web_page_preview=True,
                           reply_markup=get_events_list_keyboard(data.get("current_page"),
                                                                 page_size,
                                                                 data.get("events")))


@dp.callback_query_handler(text_contains="event_list")
async def get_event_page(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    button_type = query_data[1]

    if button_type == "done":
        await query.message.delete()
        await state.finish()
        return

    data = await state.get_data()
    if button_type == "next":
        await state.update_data(current_page=data.get("current_page") + 1)
    elif button_type == "back":
        await state.update_data(current_page=data.get("current_page") - 1)
    data = await state.get_data()
    events = data.get("events")
    current_page = data.get("current_page")
    page_size = data.get("page_size")
    start_index, end_index = get_indexes(events, current_page, page_size)
    new_message_text = ""

    for i in range(start_index, end_index + 1):
        new_message_text += create_event_messsage(events[i])
        new_message_text += "---------------------------\n\n"

    await query.message.edit_text(text=new_message_text,
                                  disable_web_page_preview=True,
                                  reply_markup=get_events_list_keyboard(current_page,
                                                                        page_size,
                                                                        events))
