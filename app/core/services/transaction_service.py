from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models.transaction import Transaction
from core.schemas.transaction import BaseTransactionCreate, BaseTransactionUpdate

class TransactionService:
    @staticmethod
    async def get_transactions(db: AsyncSession, user_id: int):
        result = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def create_transaction(db: AsyncSession, transaction_data: BaseTransactionCreate, user_id: int):
        new_transaction = Transaction(**transaction_data.dict(), user_id=user_id)
        db.add(new_transaction)
        await db.commit()
        await db.refresh(new_transaction)
        return new_transaction

    @staticmethod
    async def update_transaction(db: AsyncSession, transaction_id: int, transaction_data: BaseTransactionUpdate,
                                 user_id: int):
        transaction = await db.get(Transaction, transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise HTTPException(status_code=404, detail="Transaction not found")
        for key, value in transaction_data.dict(exclude_unset=True).items():
            setattr(transaction, key, value)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @staticmethod
    async def delete_transaction(db: AsyncSession, transaction_id: int, user_id: int):
        transaction = await db.get(Transaction, transaction_id)
        if not transaction or transaction.user_id != user_id:
            raise HTTPException(status_code=404, detail="Transaction not found")
        await db.delete(transaction)
        await db.commit()
        return {"detail": "Transaction deleted"}
