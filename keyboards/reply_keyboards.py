# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# def get_main_test()-> ReplyKeyboardMarkup:
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="Test")],
#         ],
#         resize_keyboard=True
#
#     )
#     return keyboard
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_test() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ℹ️ Про нас")],  # Ось тут твоя reply-кнопка
            [KeyboardButton(text="Test")]          # Можеш додати інші кнопки
        ],
        resize_keyboard=True
    )
    return keyboard
