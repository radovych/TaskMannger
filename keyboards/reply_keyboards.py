
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_test() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ℹ️ Про нас")],
            [KeyboardButton(text="Test")]
        ],
        resize_keyboard=True
    )
    return keyboard
