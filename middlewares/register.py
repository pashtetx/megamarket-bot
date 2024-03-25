from .session_middleware import SessionMiddleware
from .user_middleware import UserMiddleware
from .logger_middleware import LoggerMiddleware
from .playwright_middleware import PlaywrightMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram import Dispatcher, Router
import logging


def register_middlewares(dp: Dispatcher, async_session: async_sessionmaker[AsyncSession], browser):
    """ Регистриует промежутчные приложения """
    
    middlewares = (
        SessionMiddleware(async_session=async_session),
        UserMiddleware(),
        LoggerMiddleware(),
        PlaywrightMiddleware(browser)
    )
    
    for middleware in middlewares:
        logging.info(msg=f"Register {middleware.__class__.__name__}")
        dp.update.middleware.register(middleware)