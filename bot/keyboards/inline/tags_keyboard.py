from aiogram.types import InlineKeyboardMarkup
from .callback_data import tag_data
from .generate_inline_markup import generate_inline_markup
from typing import List
from utils.parser_api import get_tags


async def generate_tags_markup(checked_tags_codes: List[int], 
                               page: int) -> InlineKeyboardMarkup:
    tags = await get_tags()
    return generate_inline_markup(tags, 
                                  checked_tags_codes, 
                                  tag_data, page)
