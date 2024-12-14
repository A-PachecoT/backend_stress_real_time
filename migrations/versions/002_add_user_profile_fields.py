"""add user profile fields

Revision ID: 002
Revises: 001
Create Date: 2024-02-20 11:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("full_name", sa.String(150), nullable=True))
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("gender", sa.String(20), nullable=True))
    op.add_column("users", sa.Column("marital_status", sa.String(20), nullable=True))
    op.add_column("users", sa.Column("occupation", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "occupation")
    op.drop_column("users", "marital_status")
    op.drop_column("users", "gender")
    op.drop_column("users", "age")
    op.drop_column("users", "full_name")
