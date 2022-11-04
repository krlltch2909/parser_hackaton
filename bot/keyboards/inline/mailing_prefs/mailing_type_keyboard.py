from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..callback_data import mailing_type_data


mailing_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Все события", 
                                 callback_data=mailing_type_data.new(type="all"))
        ],
        [
            InlineKeyboardButton("Интересующие события", 
                                  callback_data=mailing_type_data.new(type="preferences"))
        ]
    ]
)
