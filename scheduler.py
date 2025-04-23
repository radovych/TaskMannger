

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from reminders.reminders import check_deadlines

# Створення планувальника
scheduler = AsyncIOScheduler()

# Планування функції для перевірки дедлайнів кожні 10 хвилин
scheduler.add_job(check_deadlines, IntervalTrigger(minutes=10))

# Запуск планувальника у асинхронному циклі
async def start_scheduler():
    scheduler.start()

# Асинхронна функція для запуску перевірки дедлайнів
async def schedule_task_updates():
    await start_scheduler()
