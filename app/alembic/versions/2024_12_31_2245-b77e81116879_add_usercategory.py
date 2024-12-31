"""Add UserCategory

Revision ID: b77e81116879
Revises: a02e7ef02f16
Create Date: 2024-12-31 22:45:25.453177

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b77e81116879"
down_revision: Union[str, None] = "a02e7ef02f16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_categories",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("custom_name", sa.String(), nullable=True),
        sa.Column("hidden", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_user_categories_category_id_categories"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_categories_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_categories")),
    )
    op.create_index(
        op.f("ix_user_categories_id"), "user_categories", ["id"], unique=False
    )
    op.add_column("categories", sa.Column("default", sa.Boolean(), nullable=False))
    op.drop_constraint("categories_name_key", "categories", type_="unique")
    op.create_unique_constraint(op.f("uq_categories_name"), "categories", ["name"])
    op.add_column(
        "transactions",
        sa.Column("user_category_id", sa.Integer(), nullable=True),
    )
    op.drop_constraint(
        "transactions_category_id_fkey", "transactions", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_transactions_user_category_id_user_categories"),
        "transactions",
        "user_categories",
        ["user_category_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("transactions", "category_id")
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.add_column(
        "transactions",
        sa.Column("category_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_transactions_user_category_id_user_categories"),
        "transactions",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "transactions_category_id_fkey",
        "transactions",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("transactions", "user_category_id")
    op.drop_constraint(op.f("uq_categories_name"), "categories", type_="unique")
    op.create_unique_constraint("categories_name_key", "categories", ["name"])
    op.drop_column("categories", "default")
    op.drop_index(op.f("ix_user_categories_id"), table_name="user_categories")
    op.drop_table("user_categories")
