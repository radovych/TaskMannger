from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.tasks import tasks
def get_inline_keyboard() -> InlineKeyboardMarkup:
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
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from data.tasks import tasks
#
#
# def get_task_list_keyboard() -> InlineKeyboardMarkup:
#     """Формує клавіатуру зі списком завдань"""
#     keyboard = InlineKeyboardMarkup(row_width=1)  # Встановлюємо 1 кнопку в рядок
#
#     for task in tasks:
#         keyboard.add(InlineKeyboardButton(text=f"📌 {task['title']}", callback_data=f"task_{task['id']}"))
#
#     keyboard.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main"))
#
#     return keyboard
#
#
# def get_main_menu_keyboard() -> InlineKeyboardMarkup:
#     """Головне меню"""
#     keyboard = InlineKeyboardMarkup(row_width=1)
#
#     keyboard.add(
#         InlineKeyboardButton(text="📋 Список завдань", callback_data="show_tasks"),
#         InlineKeyboardButton(text="➕ Додати завдання", callback_data="add_task"),
#         InlineKeyboardButton(text="✅ Завершити завдання", callback_data="complete_task"),
#         InlineKeyboardButton(text="📌 Не виконані завдання", callback_data="incomplete_tasks"),
#         InlineKeyboardButton(text="🗑 Видалити завдання", callback_data="delete_task")
#     )
#
#     return keyboard
