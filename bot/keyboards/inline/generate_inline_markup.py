from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Union
from models.EventTag import EventTag
from models.EventType import EventType
from . import PAGE_SIZE


def generate_inline_markup(code_objects: Union[List[EventType], List[EventTag]], 
                           checked_codes: List[int],  type_data: CallbackData,
                           page: int) -> InlineKeyboardMarkup:
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index
    if (start_index + PAGE_SIZE - 1) > len(code_objects) - 1:
        end_index = len(code_objects) - 1
    elif (start_index + PAGE_SIZE - 1) < len(code_objects) - 1:
        end_index += PAGE_SIZE -1

    inline_keyboard = []
    for i in range(start_index, end_index + 1):
        code_object = code_objects[i]
        button = None
        if code_object.type_code in checked_codes:
            button = InlineKeyboardButton(text="✓ " + code_object.description, 
                callback_data=type_data.new(type_code=code_object.type_code, 
                                                  button_type="basic"))
        else:
            button = InlineKeyboardButton(text=code_object.description, 
                callback_data=type_data.new(type_code=code_object.type_code, 
                                                  button_type="basic"))

        inline_keyboard.append([button])
    
    if  start_index + PAGE_SIZE < len(code_objects) - 1 and start_index > 0:
        inline_keyboard.append([
            InlineKeyboardButton(text="<<", 
                callback_data=type_data.new(type_code=-1, button_type="back")),
            InlineKeyboardButton(text=">>", 
                callback_data=type_data.new(type_code=-1, button_type="next"))])
    elif start_index + PAGE_SIZE < len(code_objects) - 1:
        inline_keyboard.append([InlineKeyboardButton(text=">>", 
            callback_data=type_data.new(type_code=-1, 
                                              button_type="next"))])
    elif start_index + PAGE_SIZE >= len(code_objects) - 1:
        inline_keyboard.append([InlineKeyboardButton(text="<<", 
            callback_data=type_data.new(type_code=-1, 
                                              button_type="back"))])

    inline_keyboard.append([InlineKeyboardButton(text="Готово", 
            callback_data=type_data.new(type_code=-1, 
                                              button_type="done"))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
