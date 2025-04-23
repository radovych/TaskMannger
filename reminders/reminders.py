
import asyncio
import datetime
from aiogram import Bot
from os import getenv
from data.tasks import tasks  # Завантаження завдань

# Завантажуємо токен з середовища
TOKEN = getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не встановлено!")

bot = Bot(token=TOKEN)

async def check_deadlines():
    while True:
        now = datetime.datetime.now()
        for task in tasks:
            due_date = task["due_date"]

            # Якщо у due_date немає часу, додаємо "00:00"
            if len(due_date) == 10:  # Формат "YYYY-MM-DD"
                due_date += " 00:00"

            try:
                due_datetime = datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"⚠️ Некоректний формат дати у завданні: {task}")
                continue  # Пропускаємо завдання з неправильною датою

            if now >= due_datetime and not task.get("notified", False):
                user_id = task.get("user_id")
                if user_id:
                    await send_reminder(task, user_id)
                    task["notified"] = True  # Позначаємо, що сповіщення вже надіслано
                else:
                    print(f"⚠️ У завданні '{task['title']}' немає user_id!")

        await asyncio.sleep(600)  # Перевірка кожні 10 хвилин

async def send_reminder(task, user_id):
    message = f"⏳ Нагадування! Завдання \"{task['title']}\" мало бути виконане до {task['due_date']}!"
    try:
        await bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"❌ Помилка надсилання нагадування для {user_id}: {e}")

async def start_reminder_service():
    asyncio.create_task(check_deadlines())  # Створення фонової задачі для перевірки дедлайнів


