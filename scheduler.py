import asyncio
import time

async def schedule_task_updates():
    while True:
        update_overdue_tasks()
        await asyncio.sleep(600)  # Чекаємо 10 хвилин (600 секунд)
