from aiogram.fsm.state import StatesGroup, State

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_deadline = State()
    waiting_for_priority = State()

# from aiogram.fsm.state import StatesGroup, State
# from states.form_states import AddTask
#
#
#
# class Form(StatesGroup):
#     name = State()
#     age = State()
# from aiogram.fsm.state import StatesGroup, State
#
# class AddTask(StatesGroup):
#     waiting_for_title = State()
#     waiting_for_description = State()