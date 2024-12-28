"""create transactions and categories tables

Revision ID: a02e7ef02f16
Revises: 0ae73e2d21e6
Create Date: 2024-12-29 00:45:47.322021

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a02e7ef02f16"
down_revision: Union[str, None] = "0ae73e2d21e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        op.f("ix_categories_id"), "categories", ["id"], unique=False
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column(
            "transaction_type",
            sa.Enum("INCOME", "EXPENSE", "TRANSFER", name="transactiontype"),
            nullable=False,
        ),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"], ["categories.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transactions_id"), "transactions", ["id"], unique=False
    )

def downgrade() -> None:
    op.drop_index(op.f("ix_transactions_id"), table_name="transactions")
    op.drop_table("transactions")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
