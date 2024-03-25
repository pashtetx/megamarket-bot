from aiogram.fsm.state import StatesGroup, State



class CategoryMonitor(StatesGroup):
    url = State()
    cashback_percent = State()