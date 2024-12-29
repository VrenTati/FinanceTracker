from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from core.models.transaction import Transaction, TransactionType

class ReportService:
    @staticmethod
    async def get_report(
            db: AsyncSession,
            user_id: int,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
    ):
        query = select(
            func.sum(Transaction.amount).filter(Transaction.transaction_type == TransactionType.INCOME),
            func.sum(Transaction.amount).filter(Transaction.transaction_type == TransactionType.EXPENSE),
        ).where(Transaction.user_id == user_id)

        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)

        result = await db.execute(query)
        income, expense = result.one()

        return {
            "income": income or 0,
            "expense": expense or 0,
            "balance": (income or 0) - (expense or 0),
        }
