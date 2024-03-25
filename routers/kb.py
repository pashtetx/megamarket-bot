from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Subscribe(CallbackData, prefix="subscribe"):
    price: int


def subscribe_menu():
    builder = InlineKeyboardBuilder()
    
    builder.button(text="1 День - 250 Р", callback_data=Subscribe(price=250).pack())
    builder.button(text="1 Неделя - 500 Р", callback_data=Subscribe(price=500).pack())
    builder.button(text="1 Месяц - 1000 Р", callback_data=Subscribe(price=1000).pack())
    builder.button(text="1 Год - 10000 Р", callback_data=Subscribe(price=10000).pack())
    
    builder.adjust(1)
    
    return builder.as_markup()