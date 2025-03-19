# from aiogram import types
# from aiogram.types import CallbackQuery
# from keyboards.inline_keyboards import get_task_list_keyboard, get_main_menu_keyboard
# from data.tasks import tasks
# from aiogram.dispatcher.filters import Text
# from loader import dp
#
#
# @dp.callback_query_handler(Text(equals="show_tasks"))
# async def show_tasks(callback: CallbackQuery):
#     """Обробка кнопки 'Список завдань'"""
#     await callback.message.edit_text("📋 *Оберіть завдання:*", parse_mode="Markdown",
#                                      reply_markup=get_task_list_keyboard())
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith("task_"))
# async def show_task_details(callback: CallbackQuery):
#     """Обробка вибору конкретного завдання"""
#     task_id = int(callback.data.split("_")[1])
#     task = next((t for t in tasks if t["id"] == task_id), None)
#
#     if task:
#         text = f"📌 *{task['title']}*\n\n{task['description']}\n\n📅 Дата: {task['due_date']}\n⚡ Пріоритет: {task['priority']}"
#         await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_task_list_keyboard())
#
#
# @dp.callback_query_handler(Text(equals="back_to_main"))
# async def back_to_main(callback: CallbackQuery):
#     """Повернення в головне меню"""
#     await callback.message.edit_text("🔙 *Головне меню:*", parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
