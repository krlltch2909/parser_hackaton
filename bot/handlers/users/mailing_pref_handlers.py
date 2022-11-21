from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from keyboards.inline.mailing_prefs.mailing_type_keyboard import mailing_type_keyboard
from keyboards.inline.mailing_prefs.mailing_status_keyboard import mailing_status_keyboard
from states.MailingPreferencesStatesGroup import MailingPreferencesStatesGroup
from utils.database import user_preferences_collection


@dp.message_handler(Command("mailing"))
async def start_mailing_pref_setting(message: types.Message):
    await message.answer("Выберите подходящий режим получения информации о мероприятиях",
                         reply_markup=mailing_type_keyboard,
                         allow_sending_without_reply=False)
    await MailingPreferencesStatesGroup.mailing_type.set()


@dp.callback_query_handler(text_contains="mailing_type", 
                           state=MailingPreferencesStatesGroup.mailing_type)
async def get_mailing_type(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    mailing_type = query_data[1]
    user_id = query.from_user.id
    await state.update_data(mailing_type=mailing_type)
    await query.message.delete()
    await bot.send_message(user_id, "Включить рассылку?", 
                           reply_markup=mailing_status_keyboard)
    await MailingPreferencesStatesGroup.mailing_status.set()


@dp.callback_query_handler(text_contains="mailing_status",
                           state=MailingPreferencesStatesGroup.mailing_status)
async def get_mailing_status(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    data = await state.get_data()
    mailing_type = data["mailing_type"]
    mailing_status = bool(query_data[1])
    user_id = query.from_user.id

    creation_data = {
        "_id": user_id,
        "mailing_type": mailing_type,
        "mailing_status": mailing_status,
    }
    update_data = {
        "mailing_type": mailing_type,
        "mailing_status": mailing_status,
    }
    user_preferences = await user_preferences_collection.find_one({"_id": user_id})

    if user_preferences is not None:
        await user_preferences_collection.update_one(
            {"_id": user_id},
            {"$set": update_data})
    else:
        await user_preferences_collection.insert_one(creation_data)
    
    await query.message.delete()
    await state.finish()
    await bot.send_message(user_id, "Настройки сохранены!")
