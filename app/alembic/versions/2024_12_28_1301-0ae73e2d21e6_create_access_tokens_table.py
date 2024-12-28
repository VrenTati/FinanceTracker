"""Create access tokens table

Revision ID: 0ae73e2d21e6
Revises: 003c1d01f658
Create Date: 2024-12-28 13:01:46.905056

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0ae73e2d21e6"
down_revision: Union[str, None] = "003c1d01f658"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "access_tokens",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        op.f("ix_access_tokens_created_at"),
        "access_tokens",
        ["created_at"],
        unique=False,
    )
    op.drop_index("ix_user_email", table_name="user")
    op.drop_table("user")

def downgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "email",
            sa.VARCHAR(length=320),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "hashed_password",
            sa.VARCHAR(length=1024),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "is_active", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_verified", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
    )
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.drop_index(
        op.f("ix_access_tokens_created_at"), table_name="access_tokens"
    )
    op.drop_table("access_tokens")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
