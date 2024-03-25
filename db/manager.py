from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class Manager:
    """ Manager database quering """
    
    def __init__(self, model: Any) -> None:
        self.model = model
        
        self.query = None
    
    async def create(self, async_session: AsyncSession, save = True, **kwargs):
        """ Create a model object 
        :async_session param: - Async session database sqlalchemy
        :save param: - Default True, if True function at once saved object
        """
        
        model = self.model
        object_model = model(**kwargs)
        if save:
            async_session.add(object_model)
            await async_session.commit()
        return object_model

    async def get(self, async_session: AsyncSession, **kwargs):
        """ Get a model object
        :async_session param: - Async session database sqlalchemy
        """
        model = self.model
        query = select(model).where(*[getattr(model, k) == v for k, v in kwargs.items()])
        result = await async_session.execute(query)
        return result.scalar_one_or_none()

    async def get_or_create(self, async_session: AsyncSession, save = True, **kwargs):
        """ Create or get model object 
        :async_session param: - Async session database sqlalchemy
        :save param: - Default True, if True function at once saved object
        """
        result = await self.get(async_session=async_session, **kwargs)
        if result:
            return result
        else:
            return await self.create(async_session=async_session, **kwargs)