from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


events_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Все события"),
            KeyboardButton("Интересующие события")
        ],
        [
            KeyboardButton("По названию"),
            KeyboardButton("По адресу")
        ]
    ],
    resize_keyboard=True,
    selective=False
)
