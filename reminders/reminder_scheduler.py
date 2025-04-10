import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from aiogram import Bot
from aiogram.types import ParseMode
from os import getenv
from aiogram.client.default import DefaultBotProperties

# Отримання токену для бота з середовища
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Функція для надсилання повідомлення користувачеві
async def send_reminder(user_id, message):
    await bot.send_message(chat_id=user_id, text=message)

# Функція для планування нагадувань
def schedule_reminder(user_id, message, date_str):
    # Ініціалізація планувальника
    scheduler = AsyncIOScheduler()
    # Створення тригера для зазначеного часу
    trigger = DateTrigger(run_date=date_str)
    # Додавання завдання в планувальник
    scheduler.add_job(send_reminder, trigger, args=[user_id, message])
    scheduler.start()

