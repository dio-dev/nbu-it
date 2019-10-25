from aiogram.dispatcher.filters.state import State, StatesGroup
# States
class UserStates(StatesGroup):
    start = State()
    select_type = State()
    select_name = State()
    get_location = State()
    show_result = State()
