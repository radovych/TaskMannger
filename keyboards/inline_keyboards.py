
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.tasks import tasks
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_task_list_keyboard() -> InlineKeyboardMarkup:
    """Формує клавіатуру зі списком завдань"""
    keyboard = []

    # Додаємо кожне завдання окремою кнопкою
    for task in tasks:
        keyboard.append([
            InlineKeyboardButton(text=f"📌 {task['title']}", callback_data=f"task_{task['id']}")
        ])

    # Кнопка "Назад"
    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📋 Список завдань", callback_data="test_btn_1")],
        [InlineKeyboardButton(text="➕ Додати завдання", callback_data="add_task")],
        [InlineKeyboardButton(text="✅ Завершити завдання", callback_data="complete_task")],
         [InlineKeyboardButton(text="📌 Не виконані завдання", callback_data="incomplete_tasks")],
         [InlineKeyboardButton(text="🗑 Видалити завдання", callback_data="delete_task")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_task_actions_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """Кнопки для взаємодії з конкретним завданням"""
    keyboard = [
        [InlineKeyboardButton(text="✏ Редагувати", callback_data=f"edit_task_{task_id}")],
        [InlineKeyboardButton(text="✅ Виконано", callback_data=f"complete_task_{task_id}")],
        [InlineKeyboardButton(text="⬅ Назад до списку", callback_data="test_btn_1")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)