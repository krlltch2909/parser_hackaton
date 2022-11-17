from aiogram.types import InlineKeyboardMarkup
from typing import List
from ..callback_data import event_type_data
from ..pref_inline_keyboard import generate_events_pref_inline_keyboard
from utils.parser_api import get_events_types


async def generate_events_types_markup(checked_types_codes: List[int],
                                 page: int) -> InlineKeyboardMarkup:
    events_types = await get_events_types()
    return generate_events_pref_inline_keyboard(events_types,
                                         checked_types_codes,
                                         event_type_data,
                                         page)
