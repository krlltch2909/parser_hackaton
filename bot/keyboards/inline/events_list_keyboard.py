from aiogram.types import InlineKeyboardMarkup
from .utils import add_control_buttons
from .callback_data import event_list_data


def get_events_list_keyboard(current_page: int, 
                             page_size: int, 
                             events: list) -> InlineKeyboardMarkup:
    start_index = (current_page - 1) * page_size
    inline_keyboard = []
    
    add_control_buttons(inline_keyboard, events, event_list_data, {}, start_index, page_size)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
