# import asyncio
# import time
#
# async def schedule_task_updates():
#     while True:
#         update_overdue_tasks()
#         await asyncio.sleep(600)  # Чекаємо 10 хвилин (600 секунд)

# import asyncio
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from datetime import datetime
#
# from data.tasks import tasks  # Ваші завдання
#
# # Створення планувальника
# scheduler = AsyncIOScheduler()
#
# # Приклад функції для оновлення завдань
# async def update_overdue_tasks():
#     # Логіка для оновлення прострочених завдань
#     pass
#
# # Планування виконання функції кожні 10 хвилин
# scheduler.add_job(update_overdue_tasks, IntervalTrigger(minutes=10))
#
# # Запуск планувальника у асинхронному циклі
# def start_scheduler():
#     scheduler.start()
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()  # Отримуємо поточний цикл подій
#     loop.create_task(start_scheduler())  # Створюємо задачу на запуск планувальника
#     loop.run_forever()  # Запускаємо цикл подій

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
