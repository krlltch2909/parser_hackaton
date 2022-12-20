from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import action_button_data


cancel_action_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Отменить", 
                                 callback_data=action_button_data.new(type="cancel"))
        ]
    ]
)
