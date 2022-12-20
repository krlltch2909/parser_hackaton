from keyboards.inline.events_prefs import *
from .handlers_utils import try_delete_cancel_message
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.PreferencesStatesGroup import PreferencesStatesGroup
from models.User import User


@dp.message_handler(Command("preferences"))
async def start_pref_setting(message: types.Message, state: FSMContext):
    user = await User.init_user(message.from_user.id)
    await user.save_to_state(state)
    await state.update_data(current_page=1)
    
    message = await message.answer("Выберите интересующие вас виды мероприятий:",
                                   reply_markup=await generate_events_types_markup(user.events_types, 
                                                                                   1))
    await state.update_data(blocking_message_id=message.message_id)
    await PreferencesStatesGroup.events_types.set()


# Получаем новый тип мероприятия.
# Сохраняем его в машину состояний и изменяем разметку
@dp.callback_query_handler(text_contains="event_type",
                           state=PreferencesStatesGroup.events_types)
async def accept_event_type(query: types.CallbackQuery, state: FSMContext):
    callback_data = query.data
    button_data = callback_data.split(":")
    type_code = int(button_data[1])
    str_page_number = button_data[2]
    
    data = await state.get_data()
    user: User = data["user_data"]
    
    # Если передаем None, значит нажата кнопка с типом мероприятия
    if str_page_number == "None":
        user.tick_event_type(type_code)
        await user.save_to_state(state)
        await query.message.\
            edit_reply_markup(await generate_events_types_markup(user.events_types,
                                                                 data["current_page"]))
        return
    
    page_number = int(str_page_number)
    
    # Если номер страницы = -1, то перейти к установке тегов
    if page_number == -1:
        # Сброс номера страницы для выбора тегов
        await state.update_data(current_page=1)
        await query.message.delete()

        message = await bot.send_message(chat_id=user.id,
                                         text="Выберите теги для фильтрации " \
                                              "интересующих мероприятий:",
                                         reply_markup=await generate_tags_markup(user.tags, 
                                                                                 1))
        await state.update_data(blocking_message_id=message.message_id)
        await try_delete_cancel_message(state)
        await PreferencesStatesGroup.tags.set()
        return
    
    await query.message.\
        edit_reply_markup(await generate_events_types_markup(user.events_types,
                                                             page_number))
    await state.update_data(current_page=page_number)
    await PreferencesStatesGroup.events_types.set()


# Получаем и сохраняем новые теги
@dp.callback_query_handler(text_contains="event_tag", state=PreferencesStatesGroup.tags)
async def accept_tag(query: types.CallbackQuery, state: FSMContext):
    callback_data = query.data
    button_data = callback_data.split(":")
    tag_code = int(button_data[1])
    str_page_number = button_data[2]
    
    data = await state.get_data()
    user: User = data["user_data"]

    if str_page_number == "None":
        async with state.proxy() as data:
            user.tick_tag(tag_code)
            await user.save_to_state(state)

        await query.message.edit_reply_markup(await generate_tags_markup(user.tags,
                                              data["current_page"]))
        return
    
    page_number = int(str_page_number)
    
    if page_number == -1:
        await user.save_to_db()
        await query.message.delete()
        await bot.send_message(chat_id=user.id, 
                               text="Настройки успешно сохранены")
        await try_delete_cancel_message(state)
        await state.finish()    
        return

    await query.message.edit_reply_markup(await generate_tags_markup(user.tags,
                                                                     page_number))
    await state.update_data(current_page=page_number)
    await PreferencesStatesGroup.tags.set()
