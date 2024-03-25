from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging


class PlaywrightMiddleware(BaseMiddleware):
    
    def __init__(self, browser) -> None:
        self.browser = browser
        super().__init__()
    
    async def __call__(self, handler, event, data):
        data["browser"] = self.browser
        return await handler(event, data)