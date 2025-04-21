

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import re
from keyboards.inline_keyboards import get_task_list_keyboard, get_main_menu_keyboard, get_delete_task_keyboard
from data.tasks import tasks
from utils import validate_deadline


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
            f"📅 Дата: {task['due_date']}\n"  # Дата вже включає годину та хвилини
            f"⚡ Пріоритет: {task['priority']}"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[  # Кнопки для редагування/видалення
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
    await message.answer("📅 Введіть дату дедлайну (у форматі РРРР-ММ-ДД-HH:mm):")
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


def get_task_list_keyboard() -> InlineKeyboardMarkup:
    priority_order = {"high": 3, "medium": 2, "low": 1}
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"], 0), reverse=True)

    keyboard = []
    for task in sorted_tasks:
        # Оновлюємо формат кнопки, щоб вказати точний час
        keyboard.append([
            InlineKeyboardButton(text=f"📌 {task['title']} (⚡ {task['priority']} - {task['due_date']})", callback_data=f"task_{task['id']}")
        ])

    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")
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




# === Завершення завдання ===
@router.callback_query(F.data.startswith("complete_task_"))
async def complete_task(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[2])
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task:
        task["completed"] = True  # Позначаємо завдання як виконане
        await callback_query.message.edit_text(
            f"✅ Завдання \"{task['title']}\" завершено!",
            reply_markup=get_task_list_keyboard()
        )
    else:
        await callback_query.message.answer("❌ Помилка: завдання не знайдено.")

# === Відображення завершених завдань ===
@router.callback_query(F.data == "completed_tasks")
async def show_completed_tasks(callback_query: types.CallbackQuery):
    completed = [task for task in tasks if task.get("completed")]

    if not completed:
        await callback_query.message.answer("❌ Немає завершених завдань.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=task["title"], callback_data=f"task_{task['id']}")] for task in completed
    ] + [[InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]])

    await callback_query.message.edit_text("✅ *Завершені завдання:*", parse_mode="Markdown", reply_markup=keyboard)


# === Вибір завдання для завершення ===
@router.callback_query(F.data == "complete_task")
async def choose_task_to_complete(callback_query: types.CallbackQuery):
    incomplete_tasks = [task for task in tasks if not task.get("completed")]

    if not incomplete_tasks:
        await callback_query.message.answer("✅ Всі завдання виконані!")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📌 {task['title']}", callback_data=f"complete_task_{task['id']}")] for task in incomplete_tasks
    ] + [[InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]])

    await callback_query.message.edit_text("📝 *Оберіть завдання для завершення:*", parse_mode="Markdown", reply_markup=keyboard)

# === Позначення завдання як завершеного ===
@router.callback_query(F.data.startswith("complete_task_"))
async def complete_task(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split("_")[2])
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task:
        task["completed"] = True  # Позначаємо завдання як виконане
        await callback_query.message.edit_text(
            f"✅ Завдання \"{task['title']}\" завершено!",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await callback_query.message.answer("❌ Помилка: завдання не знайдено.")


@router.callback_query(F.data == "incomplete_tasks")
async def show_incomplete_tasks(callback_query: types.CallbackQuery):
    incomplete = [task for task in tasks if not task.get("completed")]

    if not incomplete:
        await callback_query.message.answer("✅ Всі завдання виконані!")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📌 {task['title']}", callback_data=f"task_{task['id']}")] for task in incomplete
    ] + [[InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main")]])

    await callback_query.message.edit_text("📌 *Не виконані завдання:*", parse_mode="Markdown", reply_markup=keyboard)

@router.message(AddTaskState.waiting_for_due_date)
async def task_due_date_entered(message: Message, state: FSMContext):
    await state.update_data(due_date=message.text)  # Новий формат дедлайну з часом
    await message.answer("⚡ Введіть пріоритет (low, medium або high):")
    await state.set_state(AddTaskState.waiting_for_priority)



@router.message(F.text == "ℹ️ Про нас")
async def about_us_handler(message: Message):
    await message.answer("Ми — команда, яка створила цього бота 💬\nЗв'яжіться з нами: @nazark0wxx")

from datetime import datetime



# Перевірка формату дати
def validate_due_date(due_date: str) -> bool:
    # Перевірка формату дати "YYYY-MM-DD-HH:mm"
    if not re.match(r"^\d{4}-\d{2}-\d{2}-\d{2}:\d{2}$", due_date):
        return False
    try:
        # Перевірка, чи дата не в минулому
        deadline = datetime.strptime(due_date, "%Y-%m-%d-%H:%M")
        if deadline < datetime.now():
            return False
    except ValueError:
        return False
    return True

# Перевірка пріоритету
def validate_priority(priority: str) -> bool:
    return priority.lower() in ["low", "medium", "high"]

# Перевірка довжини тексту
def validate_length(text: str, max_length: int) -> bool:
    return len(text) <= max_length

# === Початок додавання нового завдання ===
@router.callback_query(F.data == "add_task")
async def start_add_task(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("📝 Введіть назву завдання:")
    await state.set_state(AddTaskState.waiting_for_title)

@router.message(AddTaskState.waiting_for_title)
async def task_title_entered(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("❌ Назва завдання не може бути порожньою. Спробуйте ще раз.")
        return
    if not validate_length(title, 100):
        await message.answer("❌ Назва завдання не може перевищувати 100 символів. Спробуйте ще раз.")
        return
    await state.update_data(title=title)
    await message.answer("🖊 Введіть опис завдання:")
    await state.set_state(AddTaskState.waiting_for_description)

@router.message(AddTaskState.waiting_for_description)
async def task_description_entered(message: Message, state: FSMContext):
    description = message.text.strip()
    if not description:
        await message.answer("❌ Опис завдання не може бути порожнім. Спробуйте ще раз.")
        return
    if not validate_length(description, 500):
        await message.answer("❌ Опис завдання не може перевищувати 500 символів. Спробуйте ще раз.")
        return
    await state.update_data(description=description)
    await message.answer("📅 Введіть дату дедлайну (у форматі РРРР-ММ-ДД-ГГ:хх):")
    await state.set_state(AddTaskState.waiting_for_due_date)

@router.message(AddTaskState.waiting_for_due_date)
async def task_due_date_entered(message: Message, state: FSMContext):
    due_date = message.text.strip()
    if not validate_due_date(due_date):
        await message.answer("❌ Невірний формат дати або дата в минулому. Використовуйте формат: РРРР-ММ-ДД-ГГ:хх (наприклад, 2025-04-21-14:30).")
        return
    await state.update_data(due_date=due_date)
    await message.answer("⚡ Введіть пріоритет (low, medium або high):")
    await state.set_state(AddTaskState.waiting_for_priority)

@router.message(AddTaskState.waiting_for_priority)
async def task_priority_entered(message: Message, state: FSMContext):
    priority = message.text.strip().lower()
    if not validate_priority(priority):
        await message.answer("❌ Невірний пріоритет. Виберіть один з варіантів: low, medium або high.")
        return
    await state.update_data(priority=priority)
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

# === Повернення в головне меню ===
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🔙 *Головне меню:*",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )


from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
  # Перевірка введеного дедлайну

# Створення хендлерів для додавання завдань
async def add_task_handler(message: types.Message, state: FSMContext):
    # Ваша логіка для додавання завдання
    await message.answer("Введіть заголовок завдання:")

# Хендлер для введення дедлайну
async def process_deadline_handler(message: types.Message, state: FSMContext):
    deadline = message.text.strip()
    if not validate_deadline(deadline):
        await message.answer("Невірний формат дати. Введіть дату у форматі YYYY-MM-DD.")
        return
    # Оновлення стану з введеним дедлайном
    await state.update_data(deadline=deadline)
    await message.answer("Дедлайн прийнятий! Введіть пріоритет завдання.")
    await AddTask.waiting_for_priority.set()


from aiogram import Dispatcher

# Ваші хендлери, FSM та інше

def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.answer("Hello, world!")




