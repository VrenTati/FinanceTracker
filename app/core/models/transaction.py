from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .category import Category


class TransactionType(PyEnum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class Transaction(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[UserIdType] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions", lazy="selectin"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="transactions", lazy="selectin"
    )
