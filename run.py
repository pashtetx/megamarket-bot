from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import load_config
from db.setup_db import setup_db

from middlewares.register import register_middlewares
from routers.register import register_handlers

from playwright import async_api

import asyncio
import logging


async def start():
    
    # Загружаем конфиг
    config = load_config()
    
    if config.get("Settings", "Debug"):
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(asctime)s %(message)s")
    
    bot = Bot(token=config.get("Bot", "Token"), default=DefaultBotProperties(
        parse_mode="HTML"
    ))
    
    dp = Dispatcher()
    
    sessionmaker = await setup_db(config.get("Database", "URL"))
    async with async_api.async_playwright() as playwright:
        browser = await playwright.firefox.launch()
        register_middlewares(dp, sessionmaker, browser)
        register_handlers(dp)
        
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())