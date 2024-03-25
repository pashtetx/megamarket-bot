from typing import Any, Awaitable, Callable, Coroutine, Dict
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class SessionMiddleware(BaseMiddleware):
    
    def __init__(self, async_session: async_sessionmaker[AsyncSession]) -> None:
        self.async_session = async_session
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.async_session() as session:
            data["session"] = session
        return await handler(event, data)