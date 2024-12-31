from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.fastapi_users import current_user
from core.config import settings
from core.models import db_helper, User
from core.schemas.transaction import (
    BaseTransaction,
    BaseTransactionCreate,
    BaseTransactionUpdate,
)
from core.services.transaction_service import TransactionService

router = APIRouter(prefix=settings.api.v1.transactions)


@router.get("/", response_model=list[BaseTransaction])
async def get_transactions(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    user_id = user.id
    return await TransactionService.get_transactions(db, user_id)


@router.post("/", response_model=BaseTransaction)
async def create_transaction(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    transaction: BaseTransactionCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(current_user),
):
    return await TransactionService.create_transaction(db, transaction, user_id)


@router.put("/{transaction_id}", response_model=BaseTransaction)
async def update_transaction(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    transaction_id: int,
    transaction: BaseTransactionUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(current_user),
):
    return await TransactionService.update_transaction(
        db, transaction_id, transaction, user_id
    )


@router.delete("/{transaction_id}")
async def delete_transaction(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    transaction_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user_id: int = Depends(current_user),
):
    return await TransactionService.delete_transaction(db, transaction_id, user_id)
