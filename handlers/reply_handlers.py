from aiogram import types, Router
from keyboards.inline_keyboards import get_main_menu_keyboard


router = Router()


@router.message(lambda message: message.text == "Test")
async def test_handler(message: types.Message):
    print(message)
    await message.answer("""It`s test message!""", reply_markup=get_main_menu_keyboard())

