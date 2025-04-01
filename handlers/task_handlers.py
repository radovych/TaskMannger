

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from keyboards.inline_keyboards import get_task_list_keyboard, get_main_menu_keyboard, get_delete_task_keyboard
from data.tasks import tasks
# from data.tasks import load_tasks, save_tasks

router = Router()

# === FSM States ===
class AddTaskState(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_due_date = State()
    waiting_for_priority = State()

class EditTaskState(StatesGroup):
    waiting_for_new_title = State()
    waiting_for_new_description = State()
    waiting_for_new_due_date = State()
    waiting_for_new_priority = State()

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
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✏ Редагувати", callback_data=f"edit_task_{task_id}")],
            [InlineKeyboardButton(text="🗑 Видалити", callback_data=f"delete_{task_id}")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="test_btn_1")]
        ])
        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

# === Почати редагування завдання ===
@router.callback_query(F.data.startswith("edit_task_"))
async def edit_task_start(callback_query: types.CallbackQuery, state: FSMContext):
    task_id = int(callback_query.data.split("_")[2])
    await state.update_data(task_id=task_id)
    await callback_query.message.answer("✏ Введіть нову назву завдання:")
    await state.set_state(EditTaskState.waiting_for_new_title)

@router.message(EditTaskState.waiting_for_new_title)
async def edit_task_title(message: Message, state: FSMContext):
    await state.update_data(new_title=message.text)
    await message.answer("🖊 Введіть новий опис завдання:")
    await state.set_state(EditTaskState.waiting_for_new_description)

@router.message(EditTaskState.waiting_for_new_description)
async def edit_task_description(message: Message, state: FSMContext):
    await state.update_data(new_description=message.text)
    await message.answer("📅 Введіть нову дату дедлайну (у форматі РРРР-ММ-ДД):")
    await state.set_state(EditTaskState.waiting_for_new_due_date)

@router.message(EditTaskState.waiting_for_new_due_date)
async def edit_task_due_date(message: Message, state: FSMContext):
    await state.update_data(new_due_date=message.text)
    await message.answer("⚡ Введіть новий пріоритет (low, medium або high):")
    await state.set_state(EditTaskState.waiting_for_new_priority)

@router.message(EditTaskState.waiting_for_new_priority)
async def edit_task_priority(message: Message, state: FSMContext):
    await state.update_data(new_priority=message.text)
    data = await state.get_data()

    task_id = data['task_id']
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task:
        task["title"] = data['new_title']
        task["description"] = data['new_description']
        task["due_date"] = data['new_due_date']
        task["priority"] = data['new_priority']

        await message.answer("✅ Завдання успішно оновлено!", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer("❌ Помилка: завдання не знайдено.")

    await state.clear()

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

@router.message(AddTaskState.waiting_for_title)
async def task_title_entered(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("🖊 Введіть опис завдання:")
    await state.set_state(AddTaskState.waiting_for_description)

@router.message(AddTaskState.waiting_for_description)
async def task_description_entered(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📅 Введіть дату дедлайну (у форматі РРРР-ММ-ДД):")
    await state.set_state(AddTaskState.waiting_for_due_date)

@router.message(AddTaskState.waiting_for_due_date)
async def task_due_date_entered(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)
    await message.answer("⚡ Введіть пріоритет (low, medium або high):")
    await state.set_state(AddTaskState.waiting_for_priority)

@router.message(AddTaskState.waiting_for_priority)
async def task_priority_entered(message: Message, state: FSMContext):
    await state.update_data(priority=message.text)
    data = await state.get_data()

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

# === Обробка натискання кнопки "🗑 Видалити завдання" ===
@router.callback_query(F.data == "delete_task")
async def choose_task_to_delete(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🗑 *Оберіть завдання для видалення:*",
        parse_mode="Markdown",
        reply_markup=get_delete_task_keyboard()
    )

# === Видалення конкретного завдання ===
@router.callback_query(F.data.startswith("delete_"))
async def delete_task(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[1])

    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]

    await callback_query.message.edit_text(
        "✅ Завдання було видалено.",
        reply_markup=get_task_list_keyboard()
    )
    print(tasks)


# === Обробка натискання кнопки "ℹ️ Про нас" ===
@router.callback_query(F.data == "nnn_company")
async def about_company(callback_query: types.CallbackQuery):
    text = ("ℹ️ *Про нас*\n\nnnn\\_company"
            "   & inst:nazark0wx")

    await callback_query.message.edit_text(
        text,
        parse_mode="MarkdownV2",
        reply_markup=get_main_menu_keyboard()
    )


def get_task_list_keyboard() -> InlineKeyboardMarkup:
    priority_order = {"high": 3, "medium": 2, "low": 1}
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"], 0), reverse=True)

    keyboard = []
    for task in sorted_tasks:
        keyboard.append([
            InlineKeyboardButton(text=f"📌 {task['title']} (⚡ {task['priority']})", callback_data=f"task_{task['id']}")
        ])

    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")
    ])
    keyboard.append([
        InlineKeyboardButton(text="ℹ️ Про нас", callback_data="nnn_company")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)



@router.callback_query(F.data.startswith("delete_"))
async def delete_task_handler(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[1])

    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]

    # **Оновлюємо id у списку**
    for index, task in enumerate(tasks):
        task["id"] = index + 1

    save_tasks(tasks)

    await callback_query.message.edit_text(
        "✅ Завдання було видалено.\nОновлений список завдань:",
        reply_markup=get_task_list_keyboard()
    )

