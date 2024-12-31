from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_int_pk_mixin import IdIntPKMixin

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .transaction import Transaction


class UserCategory(Base, IdIntPKMixin):
    __tablename__ = "user_categories"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    custom_name: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(
        "User", back_populates="user_categories", lazy="selectin"
    )
    base_category: Mapped["Category"] = relationship(
        "Category", back_populates="user_categories", lazy="selectin"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user_category", lazy="selectin"
    )
