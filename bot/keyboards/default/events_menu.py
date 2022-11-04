from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


events_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Все события"),
            KeyboardButton("Интересующие события")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    selective=False
)
