from typing import List
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def add_control_buttons(inline_keyboard: List[InlineKeyboardButton], 
                        objects: List, 
                        data: CallbackData, 
                        data_params: dict,
                        start_index: int, 
                        page_size: int) -> None:
    
    if (start_index + page_size - 1 <= len(objects) - 1) and (start_index > 0):
        inline_keyboard.append([
            InlineKeyboardButton(text="<<", 
                callback_data=data.new(**data_params, button_type="back")),
            InlineKeyboardButton(text=">>", 
                callback_data=data.new(**data_params, button_type="next"))])
    elif start_index + page_size < len(objects) - 1:
        inline_keyboard.append([InlineKeyboardButton(text=">>", 
            callback_data=data.new(**data_params, button_type="next"))])
    elif start_index + page_size > len(objects) - 1 and len(objects) > page_size:
        inline_keyboard.append([InlineKeyboardButton(text="<<", 
            callback_data=data.new(**data_params , button_type="back"))])
    inline_keyboard.append([InlineKeyboardButton(text="Готово", 
            callback_data=data.new(**data_params, button_type="done"))])
