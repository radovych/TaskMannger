from aiogram import Dispatcher
from .reply_handlers import router as reply_router
from .inline_handlers import router as inline_router
from .task_handlers import router as task_router
from .task_handlers import register_handlers
from .reminder_handlers import router as reminder_router

def register_handlers(dp):
    dp.include_router(reminder_router)

def register_handlers(dp: Dispatcher):
    dp.include_router(reply_router)
    dp.include_router(inline_router)
    dp.include_router(task_router)

