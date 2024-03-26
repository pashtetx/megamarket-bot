from .base import Base
from sqlalchemy import UUID, Column, BigInteger, select, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime


class Subscription(Base):
    """ Модель подписки """
    
    __tablename__ = "subscriptions"
    
    id = Column("id", UUID, default=uuid4, primary_key=True)
    expires_in = Column("expires_in", DateTime, default=datetime.now)
    user_id = Column("user_id", ForeignKey("users.id"), unique=True)
    user = relationship("User", uselist=False, back_populates="subscription", lazy="selectin")

    def __str__(self) -> str:
        return f"<Subscription id={self.id}, user={self.user.id}>"

class User(Base):
    """ Модель пользователя """
    
    __tablename__ = "users"
    
    id = Column("id", UUID, default=uuid4, primary_key=True)
    telegram_id = Column("telegram_id", BigInteger)
    subscription = relationship("Subscription",uselist=False, back_populates="user", lazy="selectin")
    is_parsing = Column("is_parsing", Boolean, default=False)
    
    def __str__(self) -> str:
        return f"<User id={self.id}, telegram_id={self.telegram_id}>"