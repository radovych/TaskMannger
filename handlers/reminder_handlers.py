from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

router = Router()

# Хендлер на команду /remind
@router.message(Command("remind"))
async def show_reminder_button(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Нагадати через 1 хвилину", callback_data="remind_in_1_minute")]
    ])
    await message.answer("Оберіть опцію нагадування:", reply_markup=keyboard)

# Callback обробник
@router.callback_query(F.data == "remind_in_1_minute")
async def remind_after_1_minute(callback: CallbackQuery):
    await callback.answer("Добре! Нагадаю через 1 хвилину ⏳")
    await asyncio.sleep(60)
    await callback.message.answer("🔔 Нагадування: не забудьте про завдання!")
