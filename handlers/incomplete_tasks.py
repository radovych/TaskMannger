from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.task_utils import get_overdue_tasks

router = Router()


@router.callback_query(lambda c: c.data == "incomplete_tasks")
async def show_overdue_tasks(callback: types.CallbackQuery):
    overdue_tasks = get_overdue_tasks()

    if not overdue_tasks:
        await callback.message.answer("✅ У вас немає прострочених завдань!")
        return

    text = "❗ *Прострочені завдання:*\n\n"
    for task in overdue_tasks:
        text += f"📌 *{task['title']}* (Дедлайн: {task['due_date']})\n"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
