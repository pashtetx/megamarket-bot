from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Router
from aiogram.filters.command import CommandStart, CommandObject, Command
from megamarket.queries import parse_products
from utils.urls import is_catalog_url
from utils.send import send_products
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from playwright.async_api import Error

from .kb import subscribe_menu, Subscribe

import asyncio

async def start(message: Message):
    await message.answer("Привет!\n 👋 Этот бот для мониторинга кешбека в интернет магазине <b>megamarket.ru</b>.")

async def parse_megamarket(message: Message, command: CommandObject, bot: Bot, session: AsyncSession, user: User, browser):
    args = command.args
    
    if not args:
        return await message.answer("❌ Укажите ссылку и кешбек")
    
    url, cashback = args.split(" ")
    cashback = int(cashback)
    
    if cashback <= 20:
        return await message.answer("❌ Минимальный кешбек 20%")

    if cashback >= 90:
        return await message.answer("❌ Максимальный кешбек 90%")
    
    if not is_catalog_url(url=url):
        return await message.answer("❌ Ссылка не корректна!")

    user.is_parsing = True
    await user.save(session)
    
    try:
        await send_products(bot, session, message.chat.id, url, cashback, browser)
    except TimeoutError:
        await message.answer("TimeoutError")


async def subscribe_buy(message: Message):
    await message.answer("<b>Тарифы</b>\n\n<i>возврат средств невозможен.</i>", reply_markup=subscribe_menu())

async def parse_stop(message: Message, user: User, session: AsyncSession):
    if user.is_parsing:
        user.is_parsing = False
        await user.save(session)
        
        return await message.answer("✅ Вы успешно остановили парсер")
    await message.answer("❌ У вас нету активных парсеров.")

def register_user_handlers(router: Router):
    router.message.register(start, CommandStart())
    router.message.register(parse_megamarket, Command("parse"))
    router.message.register(subscribe_buy, Command("buy"))
    router.message.register(parse_stop, Command("stop"))