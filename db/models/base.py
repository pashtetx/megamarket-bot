from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from ..manager import Manager

class Base(DeclarativeBase, AsyncAttrs):
    

    @classmethod
    @property
    def objects(cls) -> Manager:
        return Manager(cls)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        session.expire(self)