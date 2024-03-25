from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.models.user import User, Subscription

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        session = data["session"]
        user = await User.objects.get_or_create(session, telegram_id=data['event_from_user'].id)
        if not user.subscription:
            await Subscription.objects.create(session, user=user)
        data["user"] = user
        return await handler(event, data)