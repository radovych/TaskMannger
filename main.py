






import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from reminders.reminders import check_deadlines
from scheduler import schedule_task_updates
from keyboards.reply_keyboards import get_main_test
from dotenv import load_dotenv
from os import getenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

# Налаштування зберігання сесії
storage = MemoryStorage()

# Отримуємо токен з середовища
TOKEN = getenv("BOT_TOKEN")

# Ініціалізація бота
bot = Bot(token=TOKEN)

# Ініціалізація диспетчера з параметрами бота та сховища
dp = Dispatcher(storage=storage)

# Регістрація хендлерів
register_handlers(dp)

# Хендлер для команди /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=get_main_test())

# Асинхронна функція для запуску перевірки дедлайнів
async def run_check_deadlines():
    while True:
        await check_deadlines()
        await asyncio.sleep(60)  # Перевірка кожні 60 секунд

# Основна функція для запуску бота
async def main():
    # Запуск фонових задач
    asyncio.create_task(run_check_deadlines())  # Запускаємо перевірку дедлайнів у фоні
    asyncio.create_task(schedule_task_updates())  # Запускаємо планування оновлень

    # Запуск бота
    await dp.start_polling(bot)

# Головна точка входу
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


# import asyncio
# import logging
# import sys
# from aiogram import Bot, Dispatcher, html
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.fsm.storage.memory import MemoryStorage
# from handlers.task_handlers import register_handlers  # Змінили на правильний шлях
# from reminders.reminders import check_deadlines
# from scheduler import schedule_task_updates
# from keyboards.reply_keyboards import get_main_test
# from dotenv import load_dotenv
# from os import getenv
#
# # Завантажуємо змінні середовища з файлу .env
# load_dotenv()
#
# # Налаштування зберігання сесії
# storage = MemoryStorage()
#
# # Отримуємо токен з середовища
# TOKEN = getenv("BOT_TOKEN")
#
# # Ініціалізація бота
# bot = Bot(token=TOKEN)
#
# # Ініціалізація диспетчера з параметрами бота та сховища
# dp = Dispatcher(storage=storage)
#
# # Регістрація хендлерів
# register_handlers(dp)
#
# # Хендлер для команди /start
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=get_main_test())
#
# # Асинхронна функція для запуску перевірки дедлайнів
# async def run_check_deadlines():
#     while True:
#         await check_deadlines()
#         await asyncio.sleep(60)  # Перевірка кожні 60 секунд
#
# # Основна функція для запуску бота
# async def main():
#     # Запуск фонових задач
#     asyncio.create_task(run_check_deadlines())  # Запускаємо перевірку дедлайнів у фоні
#     asyncio.create_task(schedule_task_updates())  # Запускаємо планування оновлень
#
#     # Запуск бота
#     await dp.start_polling(bot)
#
# # Головна точка входу
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())







