from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_test()-> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Test")],
            [KeyboardButton(text="Test1")],
            [KeyboardButton(text="Test2")],
        ],
        resize_keyboard=True

    )
    return keyboard