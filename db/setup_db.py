from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models.base import Base
from .models.user import User, Subscription

async def setup_db(db_url: str):
    """ Иницилизация базы данных """
    
    engine = create_async_engine(db_url)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(bind=engine)
    
    return async_session
    
    