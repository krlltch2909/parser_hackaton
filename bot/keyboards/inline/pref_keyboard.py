import os
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models.EventTag import EventTag
from models.EventType import EventType
from utils.get_indexes import get_indexes
from .utils import add_control_buttons


PAGE_SIZE = os.getenv("PREF_PAGE_SIZE")
PAGE_SIZE = int(PAGE_SIZE) if PAGE_SIZE is not None else 3


def generate_events_pref_inline_keyboard(code_objects: list[EventType] | list[EventTag],
                                         checked_codes: list[int],
                                         type_data: CallbackData,
                                         current_page: int) -> InlineKeyboardMarkup:
    start_index, end_index = get_indexes(code_objects, current_page, PAGE_SIZE)
    inline_keyboard = []
    for i in range(start_index, end_index + 1):
        code_object = code_objects[i]
        button = None
        if code_object.type_code in checked_codes:
            button = InlineKeyboardButton(text="✓ " + code_object.description, 
                callback_data=type_data.new(type_code=code_object.type_code, 
                                            page_number="None"))
        else:
            button = InlineKeyboardButton(text=code_object.description, 
                callback_data=type_data.new(type_code=code_object.type_code, 
                                            page_number="None"))

        inline_keyboard.append([button])

    add_control_buttons(inline_keyboard, code_objects,
                        type_data, {"type_code": -1}, 
                        PAGE_SIZE, current_page)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
