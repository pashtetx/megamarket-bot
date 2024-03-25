from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging


class LoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data['user']
        # logging.info(msg=f"User {user.id} called handler {handler.func.__name__}")
        return await handler(event, data)