from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .user_category import UserCategory


class Category(Base, IdIntPKMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    default: Mapped[bool] = mapped_column(default=False, nullable=False)

    user_categories: Mapped[list["UserCategory"]] = relationship(
        "UserCategory", back_populates="base_category", lazy="selectin"
    )
