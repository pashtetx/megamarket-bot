from aiogram.types import Message, User, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, CallbackQuery
from aiogram import Bot, Router
from aiogram.filters.command import CommandStart, CommandObject, Command
from megamarket.queries import parse_products
from utils.urls import is_catalog_url
from utils.send import send_products
from db.models.user import User as DBUser
from sqlalchemy.ext.asyncio import AsyncSession
from playwright.async_api import Error

from .kb import subscribe_menu, Subscribe, Navigate, start_menu, back_menu
from datetime import datetime

import asyncio


async def send_profile(telegram_user: User, bot: Bot, user: DBUser):
    photo = FSInputFile(path="assets/profile_img.png")
    
    text = f"Ваш профиль:\nИмя: {telegram_user.first_name} {telegram_user.last_name}"
    text += f"\nПодписка: Закончится в { user.subscription.expires_in.strftime(format='%Y %d.%m') }" if user.subscription.expires_in > datetime.now() else "\nПодписка: Неактивна"
    
    await bot.send_photo(chat_id=telegram_user.id, photo=photo, caption=text, reply_markup=back_menu())

async def send_about(telegram_user: User, bot: Bot, *args, **kwargs):
    photo = FSInputFile(path="assets/about_img.png")
    text = f"Этот бот предназначен для парсинга данных с сайта megamarket.ru"
    await bot.send_photo(chat_id=telegram_user.id, photo=photo, caption=text, reply_markup=back_menu())

async def send_parser(telegram_user: User, bot: Bot, user: DBUser):
    photo = FSInputFile(path="assets/parse_img.png")
    if user.subscription.expires_in > datetime.now():
        text = "Чтобы парсить пропишите /parse {ссылку на каталог} {кешбек}"
        return await bot.send_photo(chat_id=telegram_user.id, photo=photo, caption=text, reply_markup=back_menu())
    return await subscribe_buy(telegram_user, bot)

async def send_help(telegram_user: User, bot: Bot, *args, **kwargs):
    photo = FSInputFile(path="assets/help_img.png")
    text = "Помощь\n\nВопросы задавать - @Aushenich"
    return await bot.send_photo(chat_id=telegram_user.id, photo=photo, caption=text, reply_markup=back_menu())

async def start(message: Message):
    photo = FSInputFile(path="assets/start_img.jpg")
    await message.answer_photo(photo=photo, caption="Как пользоваться ботом?\n1. Выбрать необходимый вариант подписки\n2. Оплатить подписку любым удобным способом\n3. После успешной оплаты для поиска необходимо написать команду /parse (ссылка на категорию) (минимальный процент кешбека)\nПример: /parse https://megamarket.ru/catalog/smartfony-apple/ 50", reply_markup=start_menu())

async def parse_megamarket(message: Message, command: CommandObject, bot: Bot, session: AsyncSession, user: DBUser, browser):
    
    if user.subscription.expires_in < datetime.now():
        return await message.answer("❌ У вас неактивная подписка!")
    
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


async def subscribe_buy(telegram_user: User, bot: Bot, *args, **kwargs):
    photo = FSInputFile("assets/subscribe_img.png")
    await bot.send_photo(photo=photo, chat_id=telegram_user.id, caption="<b>Тарифы</b>\n\n<i>возврат средств невозможен.</i>", reply_markup=subscribe_menu())


async def parse_stop(message: Message, user: User, session: AsyncSession):
    if user.is_parsing:
        user.is_parsing = False
        await user.save(session)
        
        return await message.answer("✅ Вы успешно остановили парсер")
    await message.answer("❌ У вас нету активных парсеров.")


async def navigate(callback_query: CallbackQuery, callback_data: Navigate, bot: Bot, user: User):
    func = callback_data.name
    
    if func == "back":
        await start(callback_query.message)
        await callback_query.message.delete()
        return 
    
    handlers = {
        "parsing":send_parser,
        "profile":send_profile,
        "about":send_about,
        "help":send_help
    }
    
    
    await handlers[func](callback_query.from_user, bot, user)
    await callback_query.message.delete()


def register_user_handlers(router: Router):
    router.message.register(start, CommandStart())
    router.message.register(parse_megamarket, Command("parse"))
    router.message.register(parse_stop, Command("stop"))
    router.callback_query.register(navigate, Navigate.filter())