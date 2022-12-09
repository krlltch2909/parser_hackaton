from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from keyboards.inline.mailing_prefs.mailing_type_keyboard import mailing_type_keyboard
from keyboards.inline.mailing_prefs.mailing_status_keyboard import mailing_status_keyboard
from states.MailingPreferencesStatesGroup import MailingPreferencesStatesGroup
from models.User import User


@dp.message_handler(Command("mailing"))
async def start_mailing_pref_setting(message: types.Message, state: FSMContext):
    user = await User.init_user(message.from_user.id)
    await state.update_data(user_data=user)
    await message.answer("Выберите подходящий режим получения информации о мероприятиях",
                         reply_markup=mailing_type_keyboard,
                         allow_sending_without_reply=False)
    await MailingPreferencesStatesGroup.mailing_type.set()


@dp.callback_query_handler(text_contains="mailing_type", 
                           state=MailingPreferencesStatesGroup.mailing_type)
async def get_mailing_type(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    mailing_type = query_data[1]
    user: User = (await state.get_data())["user_data"]
    user.mailing_type = mailing_type
    await user.save_to_state(state)
    await query.message.delete()
    await bot.send_message(user.id, "Включить рассылку?", 
                           reply_markup=mailing_status_keyboard)
    await MailingPreferencesStatesGroup.mailing_status.set()
    

@dp.callback_query_handler(text_contains="mailing_status",
                           state=MailingPreferencesStatesGroup.mailing_status)
async def get_mailing_status(query: types.CallbackQuery, state: FSMContext):
    query_data = query.data.split(":")
    user: User = (await state.get_data())["user_data"]
    user.mailing_status = query_data[1] == "True"
    await user.save_to_db()
    await query.message.delete()
    await state.finish()
    await bot.send_message(user.id, "Настройки сохранены!")
