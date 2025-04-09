
import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from handlers import task_handlers

import asyncio
from reminders.reminders import check_deadlines
from keyboards.reply_keyboards import get_main_test
from handlers import register_handlers
import asyncio
import time
import asyncio
from scheduler import schedule_task_updates
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
register_handlers(dp)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=get_main_test())


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


bot = Bot(token='7745283882:AAGIwwhs6gvTY4gdwuCk54FjSzBatjKAGXc')
dp = Dispatcher()

dp.include_router(task_handlers.router)

async def main():
    asyncio.create_task(check_deadlines())  # Запускаємо перевірку дедлайнів у фоні
    await dp.start_polling(bot)

asyncio.run(main())

async def main():
    asyncio.create_task(schedule_task_updates())  # Запускаємо перевірку дедлайнів
    # Інші частини коду для бота...

asyncio.run(main())
