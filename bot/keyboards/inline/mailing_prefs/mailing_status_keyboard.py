from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..callback_data import mailing_status_data


mailing_status_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data=mailing_status_data.new(status=True)),
            InlineKeyboardButton("Нет", callback_data=mailing_status_data.new(status=False)) 
        ]
    ]
)
