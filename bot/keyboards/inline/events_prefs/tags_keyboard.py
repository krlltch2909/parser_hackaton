from aiogram.types import InlineKeyboardMarkup
from ..callback_data import tag_data
from ..pref_inline_keyboard import generate_events_pref_inline_keyboard
from utils.parser_api import get_tags


async def generate_tags_markup(checked_tags_codes: list[int],
                               page: int) -> InlineKeyboardMarkup:
    tags = await get_tags()
    return generate_events_pref_inline_keyboard(tags,
                                                checked_tags_codes,
                                                tag_data, page)
