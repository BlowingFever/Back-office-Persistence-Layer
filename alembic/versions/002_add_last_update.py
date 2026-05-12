"""Added last_update attribute

Revision ID: 002_add_last_update
Revises: 001_initial_schema
Create Date: 2026-03-02 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002_add_last_update"
down_revision: Union[str, None] = "001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tables that receive last_update
_TABLES = [
    "fighter",
    "medical_record",
    "tournament",
    "tatami",
    "category",
    "fighter_category_registration",
    "match",
]


def upgrade() -> None:
    """Add last_update (nullable DateTime) to every model table."""
    for table in _TABLES:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(
                sa.Column("last_update", sa.DateTime(), nullable=True)
            )


def downgrade() -> None:
    """Remove last_update from all model tables."""
    for table in _TABLES:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column("last_update")
