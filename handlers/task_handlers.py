from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from keyboards.inline_keyboards import get_task_list_keyboard, get_main_menu_keyboard
from data.tasks import tasks

router = Router()

# === FSM States ===
class AddTaskState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_due_date = State()
    waiting_for_priority = State()

# === Показ списку завдань ===
@router.callback_query(F.data == "test_btn_1")
async def show_tasks(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "📋 *Оберіть завдання:*",
        parse_mode="Markdown",
        reply_markup=get_task_list_keyboard()
    )

# === Деталі завдання ===
@router.callback_query(F.data.startswith("task_"))
async def show_task_details(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[1])
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task:
        text = (
            f"📌 *{task['title']}*\n\n"
            f"{task['description']}\n\n"
            f"📅 Дата: {task['due_date']}\n"
            f"⚡ Пріоритет: {task['priority']}"
        )
        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_task_list_keyboard()
        )

# === Повернення в головне меню ===
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🔙 *Головне меню:*",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

# === Почати додавання нового завдання ===
@router.callback_query(F.data == "add_task")
async def start_add_task(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("📝 Введіть назву завдання:")
    await state.set_state(AddTaskState.waiting_for_title)

# === Назва завдання ===
@router.message(AddTaskState.waiting_for_title)
async def task_title_entered(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("🖊 Введіть опис завдання:")
    await state.set_state(AddTaskState.waiting_for_description)

# === Опис завдання ===
@router.message(AddTaskState.waiting_for_description)
async def task_description_entered(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📅 Введіть дату дедлайну (у форматі РРРР-ММ-ДД):")
    await state.set_state(AddTaskState.waiting_for_due_date)

# === Дата дедлайну ===
@router.message(AddTaskState.waiting_for_due_date)
async def task_due_date_entered(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    await message.answer("⚡ Введіть пріоритет (low, medium або high):")
    await state.set_state(AddTaskState.waiting_for_priority)

# === Пріоритет завдання ===
@router.message(AddTaskState.waiting_for_priority)
async def task_priority_entered(message: Message, state: FSMContext):
    await state.update_data(priority=message.text)
    data = await state.get_data()

    # Додаємо нове завдання в список
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "description": data['description'],
        "due_date": data['due_date'],
        "priority": data['priority'],
        "completed": False
    }
    tasks.append(new_task)

    await message.answer("✅ Завдання додано успішно!", reply_markup=get_main_menu_keyboard())
    await state.clear()


