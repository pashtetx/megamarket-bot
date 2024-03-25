from aiogram import Dispatcher, Router
from .handlers import register_user_handlers


def register_handlers(dp: Dispatcher):
    
    router = Router()
    
    register_user_handlers(router)
    
    dp.include_router(router)