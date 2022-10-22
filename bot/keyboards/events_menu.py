from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


events_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Все события"),
            KeyboardButton("Интересующие события")
        ],
        [
            KeyboardButton("Режим рассылки всех событий"),
            KeyboardButton("Режим рассылки интересующих событий")
        ]
    ],
    resize_keyboard=False
)
