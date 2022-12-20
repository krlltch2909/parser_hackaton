import os
from utils import *
from models import *
from keyboards.inline import *
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from .handlers_utils import cancel_message_exists
from loader import dp, bot
from keyboards.default.events_menu import events_menu
from states.EventStatesGroup import EventStatesGroup


PAGE_SIZE = os.getenv("EVENTS_PAGE_SISE")
PAGE_SIZE = int(PAGE_SIZE) if PAGE_SIZE is not None else 5


@dp.message_handler(Command("start"))
async def show_start_menu(message: types.Message):
    user_id = message.from_user.id
    await User.init_user(user_id)    
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

    data = await state.get_data()    
    # Если сообщение с виджетом перехода по страницам уже существует, 
    # то его нужно удалить для избежания конфликтов
    # с потенциально разным количеством мероприятий
    if "last_events_list_message_id" in data:
        try:
            await bot.delete_message(message.from_user.id, 
                                     data["last_events_list_message_id"])
        except MessageToDeleteNotFound:
            pass

    if message.text == "Все события":
        events.extend(await get_events())
    elif message.text == "Интересующие события":
        user = await User.init_user(message.from_user.id)

        if len(user.events_types) == 0 and len(user.tags) == 0:
            await bot.send_message(user.id,
                                   text="Вы не указали ваши предпочтения.\n"\
                                        "Воспользуйтесь командой /preferences.")
            return
        else:
            events.extend(await get_events_by_preferences(user.events_types, 
                                                          user.tags))
    await state.update_data(events=events)
    await state.update_data(page_size=PAGE_SIZE)
    await state.update_data(current_page=1)

    user_id = message.from_user.id
    await message.delete()
    result_message = ""
    data = await state.get_data()
    page_size = int(data["page_size"])
    
    if len(events) == 0:
        result_message = "Не удалось найти мероприятия"
        await bot.send_message(user_id, result_message)
    elif len(events) <= page_size:
        result_message = create_events_response(0, len(data["events"]) - 1, 
                                                data["events"])
        await bot.send_message(user_id, result_message, 
                               disable_web_page_preview=True)
    else:
        result_message = create_events_response(0, page_size-1, data["events"])
        message = await bot.send_message(user_id,
                                         result_message,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_events_list_keyboard(1,
                                                                               page_size,
                                                                               data["events"]))
        # Для отслеживания последнего сообщения с виджетом переключения страниц
        await state.update_data(last_events_list_message_id=message.message_id)


@dp.callback_query_handler(text_contains="event_list")
async def get_event_page(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    str_page_number = query_data[1]
    # Завершаем просмотр мероприятий
    if int(str_page_number) == -1:
        await query.message.delete()
        await state.finish()
        return

    data = await state.get_data()

    if "current_page" not in data:
        await query.message.delete()
        return
    
    current_page_number = data["current_page"]
    new_page_number = int(str_page_number)
    
    if new_page_number != current_page_number:
        await state.update_data(current_page=new_page_number)
        
        data = await state.get_data()
        events = data["events"]
        page_size = data["page_size"]
        start_index, end_index = get_indexes(events, new_page_number, page_size)
        new_message_text = create_events_response(start_index, end_index, events)

        await query.message.edit_text(text=new_message_text,
                                      disable_web_page_preview=True,
                                      reply_markup=get_events_list_keyboard(new_page_number,
                                                                            page_size,
                                                                            events))


@dp.message_handler(lambda message: message.text and message.text\
    in ["По названию", "По адресу"])
async def send_name_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "last_events_list_message_id" in data:
        try:
            await bot.delete_message(message.from_user.id, 
                                     data["last_events_list_message_id"])
        except MessageToDeleteNotFound:
            pass
    
    if message.text == "По названию":
        await message.answer("Введите название интересующего мероприятия")
    else:
        await message.answer("Введите адрес или его часть")
    await state.update_data(type=message.text)
    await EventStatesGroup.field.set()


@dp.message_handler(state=EventStatesGroup.field)
async def get_events_by_name(message: types.Message, state: FSMContext):
    field = message.text.lower()
    data = await state.get_data()
    type = data["type"]
    events = await get_events()
    result_events: list[Event] = []
    
    for event in events:
        if type == "По названию":
            if field in event.title.lower():
                result_events.append(event)
        else:
            if event.address is not None and \
                field in event.address.lower():
                    result_events.append(event)
    
    if len(result_events) == 0:
        result_message = "Не удалось найти мероприятия"
        await bot.send_message(message.from_user.id, result_message)
    elif len(result_events) <= PAGE_SIZE:
        result_message = create_events_response(0, len(result_events) - 1, 
                                                result_events)
        await bot.send_message(message.from_user.id, result_message, 
                               disable_web_page_preview=True)
    else:
        await state.update_data(events=result_events)
        await state.update_data(page_size=PAGE_SIZE)
        await state.update_data(current_page=1)
        result_message = create_events_response(0, PAGE_SIZE-1, result_events)
        message = await bot.send_message(message.from_user.id,
                                         result_message,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_events_list_keyboard(1, PAGE_SIZE,
                                                                               result_events))
        # Для отслеживания последнего сообщения с виджетом переключения страниц
        await state.update_data(last_events_list_message_id=message.message_id)
    await state.reset_state(with_data=False)


@dp.message_handler(state="*")
async def state_alert(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    state_data = await state.get_data()
    
    if not cancel_message_exists(state_data) and current_state != None:
        new_message = await message.answer("Сначала необходимо завершить предыдущее действие!",
                                           reply_markup=cancel_action_keyboard)
        await state.update_data(existing_cancel_message_id=new_message.message_id)
    await message.delete()
