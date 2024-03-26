from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Subscribe(CallbackData, prefix="subscribe"):
    price: int

class Navigate(CallbackData, prefix="nav"):
    name: str


def back_menu():
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Назад", callback_data=Navigate(name="back").pack())
    
    builder.adjust(1)
    
    return builder.as_markup()

def subscribe_menu():
    builder = InlineKeyboardBuilder()
    
    builder.button(text="1 День - 249 Р", callback_data=Subscribe(price=250).pack())
    builder.button(text="1 Неделя - 499 Р", callback_data=Subscribe(price=500).pack())
    builder.button(text="1 Месяц - 999 Р", callback_data=Subscribe(price=1000).pack())
    builder.button(text="1 Год - 9999 Р", callback_data=Subscribe(price=10000).pack())
    builder.button(text="Назад", callback_data=Navigate(name="back").pack())
    
    builder.adjust(1)
    
    return builder.as_markup()

def start_menu():
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Профиль", callback_data=Navigate(name="profile").pack())
    builder.button(text="О нас", callback_data=Navigate(name="about").pack())
    builder.button(text="Парсинг", callback_data=Navigate(name="parsing").pack())
    builder.button(text="Помощь", callback_data=Navigate(name="help").pack())
    
    builder.adjust(2)
    
    return builder.as_markup()