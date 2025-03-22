from aiogram import types, Router
from keyboards.inline_keyboards import get_main_menu_keyboard
from keyboards.inline_keyboards import get_task_list_keyboard

router = Router()

# @router.callback_query(lambda c: c.data.startswith("test_btn_1"))
# async def test_callback_handler(callback_query: types.CallbackQuery):
#     data = callback_query.data
#     if data == "test_btn_1":
#         await callback_query.message.answer('You pressed first Inline Button')
#     elif data == "test_btn_2":
#         await callback_query.message.delete()
#         await callback_query.message.answer('You pressed second Inline Button', reply_markup=get_main_menu_keyboard())


