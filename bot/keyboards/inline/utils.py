import math
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def add_control_buttons(inline_keyboard: list[list[InlineKeyboardButton]], 
                        objects: list, 
                        data: CallbackData, 
                        data_params: dict,
                        page_size: int,
                        current_page: int) -> None:
    """
    Добавляет к переданной inline_keyboard кнопки перехода по страницам
    """
    pages_count = math.ceil(len(objects) / page_size)
    buttons = []    
    if current_page < 4:
        if pages_count > 4:
            buttons.extend(_get_start_end_buttons(current_page, 1, 
                                                  4, data, 
                                                  data_params))
            buttons.append(InlineKeyboardButton(text=str(f"{pages_count} >>"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=pages_count)))
        else:
            buttons.extend(_get_start_end_buttons(current_page, 1, 
                                                  pages_count, data, 
                                                  data_params))
    elif (4 <= current_page <= pages_count - 3):
        buttons.append(InlineKeyboardButton(text=str(f"<< 1"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=1)))

        buttons.append(InlineKeyboardButton(text=str(f"{current_page - 1}"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=current_page - 1)))

        buttons.append(InlineKeyboardButton(text=str(f"-{current_page}-"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=current_page)))

        buttons.append(InlineKeyboardButton(text=str(f"{current_page + 1}"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=current_page + 1)))

        buttons.append(InlineKeyboardButton(text=str(f"{pages_count} >>"), 
                                                callback_data=data.new(**data_params, 
                                                                        page_number=pages_count)))
    else:
        if pages_count == 4:
            buttons.extend(_get_start_end_buttons(current_page, 1, 
                                                  4, data, 
                                                  data_params))
        else:
            buttons.append(InlineKeyboardButton(text=str(f"<< 1"), 
                                                    callback_data=data.new(**data_params, 
                                                                            page_number=1)))
            buttons.extend(_get_start_end_buttons(current_page, pages_count-3, 
                                                pages_count, data, 
                                                data_params))

    inline_keyboard.append(buttons)
    inline_keyboard.append([InlineKeyboardButton(text="Готово", 
                                                 callback_data=data.new(**data_params, 
                                                                        page_number=-1))])


def _get_start_end_buttons(current_page: int, start_page: int, 
                           pages_count: int, data: CallbackData, 
                           data_params: dict) -> list[InlineKeyboardButton]:
    buttons = []
    for i in range(start_page, pages_count + 1):
        if i == current_page:
            buttons.append(InlineKeyboardButton(text=str(f"-{i}-"), 
                                                callback_data=data.new(**data_params, 
                                                                       page_number=i))) 
        else:
            buttons.append(InlineKeyboardButton(text=str(f"{i}"), 
                                                callback_data=data.new(**data_params, 
                                                                       page_number=i))) 
    return buttons
