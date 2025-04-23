
from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.fsm.context import FSMContext


class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_deadline = State()
    waiting_for_priority = State()

# Обробка введення дедлайну
@dp.message_handler(state=AddTask.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    deadline = message.text.strip()

    if not validate_deadline(deadline):
        await message.answer("Невірний формат дати. Будь ласка, введіть дату у форматі YYYY-MM-DD.")
        return
    await state.update_data(deadline=deadline)
    await message.answer("Дедлайн підтверджено! Введіть пріоритет завдання.")
    await AddTask.waiting_for_priority.set()
