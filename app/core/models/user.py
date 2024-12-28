from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base
from core.types.user_id import UserIdType
from .mixins.id_int_pk_mixin import IdIntPKMixin

class User(Base, IdIntPKMixin, SQLAlchemyBaseUserTable[UserIdType]):
    pass

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, User)
