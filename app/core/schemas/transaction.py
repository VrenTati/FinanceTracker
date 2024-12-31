from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.models.transaction import TransactionType
from core.types.user_id import UserIdType


class BaseTransaction(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    date: date
    transaction_type: TransactionType
    category_id: Optional[int] = None
    user_id: UserIdType

    model_config = ConfigDict(from_attributes=True)


class BaseTransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    transaction_type: TransactionType
    category_id: Optional[int] = None
    user_id: UserIdType


class BaseTransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    transaction_type: Optional[TransactionType] = None
    category_id: Optional[int] = None
