from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Union
from models.EventTag import EventTag
from models.EventType import EventType
from utils.get_indexes import get_indexes
from .utils import add_control_buttons
from . import PAGE_SIZE


def generate_events_pref_inline_keyboard(code_objects: Union[List[EventType], List[EventTag]],
                                  checked_codes: List[int],
                                  type_data: CallbackData,
                                  page: int) -> InlineKeyboardMarkup:
    start_index, end_index = get_indexes(code_objects, page, PAGE_SIZE)
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

    add_control_buttons(inline_keyboard, code_objects,
                        type_data, {"type_code": -1} ,start_index, PAGE_SIZE)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
