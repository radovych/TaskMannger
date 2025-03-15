from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_test() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Список завдань", callback_data="test_btn_1")],
        [InlineKeyboardButton(text="Додати завдання", callback_data="test_btn_2")],
        [InlineKeyboardButton(text="Завершити завдання", callback_data="test_btn_3")],
         [InlineKeyboardButton(text="Не виконані завдання", callback_data="test_btn_4")],
         [InlineKeyboardButton(text="Видалити завдання", callback_data="test_btn_5")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inline_test_2() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Список завдань", callback_data="test_btn_6")],
    ]