from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped

from core.models import Base
from core.types.user_id import UserIdType
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .transaction import Transaction
    from .user_category import UserCategory


class User(Base, IdIntPKMixin, SQLAlchemyBaseUserTable[UserIdType]):
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", lazy="selectin"
    )
    user_categories: Mapped[list["UserCategory"]] = relationship(
        "UserCategory", back_populates="user", lazy="selectin"
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
