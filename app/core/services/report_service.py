import io
import os
from datetime import date
from typing import Optional
from uuid import uuid4

import matplotlib.pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from core.models.transaction import Transaction, TransactionType

class ReportService:
    @staticmethod
    async def generate_report_graphs(
            db: AsyncSession,
            user_id: int,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
    ) -> dict:
        category_data = await ReportService._get_expense_by_category(db, user_id, start_date, end_date)
        time_data = await ReportService._get_expense_by_time(db, user_id, start_date, end_date)
        heatmap_data = await ReportService._get_expense_heatmap(db, user_id, start_date, end_date)

        pie_chart = ReportService._generate_pie_chart(category_data)
        line_chart = ReportService._generate_line_chart(time_data)
        bar_chart = ReportService._generate_bar_chart(category_data)
        heatmap = ReportService._generate_heatmap(heatmap_data)

        pie_chart_path = ReportService._save_chart_locally(pie_chart, "pie_chart.png")
        line_chart_path = ReportService._save_chart_locally(line_chart, "line_chart.png")
        bar_chart_path = ReportService._save_chart_locally(bar_chart, "bar_chart.png")
        heatmap_path = ReportService._save_chart_locally(heatmap, "heatmap.png")

        return {
            "pie_chart_path": pie_chart_path,
            "line_chart_path": line_chart_path,
            "bar_chart_path": bar_chart_path,
            "heatmap_path": heatmap_path,
        }

    @staticmethod
    async def _get_expense_by_category(db, user_id, start_date, end_date):
        query = select(
            Transaction.category_id, func.sum(Transaction.amount)
        ).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).group_by(Transaction.category_id)

        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)

        result = await db.execute(query)
        return {row[0]: row[1] for row in result}

    @staticmethod
    async def _get_expense_by_time(db, user_id, start_date, end_date):
        query = select(
            Transaction.date, func.sum(Transaction.amount)
        ).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).group_by(Transaction.date).order_by(Transaction.date)

        result = await db.execute(query)
        return {row[0]: row[1] for row in result}

    @staticmethod
    async def _get_expense_heatmap(db, user_id, start_date, end_date):
        query = select(
            func.date_part("day", Transaction.date),
            func.sum(Transaction.amount)
        ).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).group_by(func.date_part("day", Transaction.date))

        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)

        result = await db.execute(query)
        return {int(row[0]): row[1] for row in result}

    @staticmethod
    def _generate_pie_chart(data: dict) -> io.BytesIO:
        labels = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        return ReportService._save_to_buffer(fig)

    @staticmethod
    def _generate_line_chart(data: dict) -> io.BytesIO:
        dates = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots()
        ax.plot(dates, values, marker='o')
        ax.set_title("Expenses Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")

        return ReportService._save_to_buffer(fig)

    @staticmethod
    def _generate_bar_chart(data: dict) -> io.BytesIO:
        categories = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_title("Expenses by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        return ReportService._save_to_buffer(fig)

    @staticmethod
    def _generate_heatmap(data: dict) -> io.BytesIO:
        days = list(range(1, 32))
        values = [data.get(day, 0) for day in days]

        fig, ax = plt.subplots()
        ax.bar(days, values)
        ax.set_title("Daily Expenses Heatmap")
        ax.set_xlabel("Day of Month")
        ax.set_ylabel("Amount")

        return ReportService._save_to_buffer(fig)

    @staticmethod
    def _save_to_buffer(fig) -> io.BytesIO:
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf

    @staticmethod
    def _save_chart_locally(image_buffer: io.BytesIO, filename: str) -> str:
        output_dir = "generated_reports"
        os.makedirs(output_dir, exist_ok=True)
        unique_filename = f"{uuid4()}-{filename}"
        file_path = os.path.join(output_dir, unique_filename)

        with open(file_path, "wb") as f:
            f.write(image_buffer.read())
        return file_path
