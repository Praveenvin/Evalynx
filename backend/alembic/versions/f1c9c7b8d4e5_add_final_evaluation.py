"""add final evaluation to interview sessions

Revision ID: f1c9c7b8d4e5
Revises: 5f1c9c7b8d4e
Create Date: 2026-08-12 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1c9c7b8d4e5'
down_revision: Union[str, None] = '5f1c9c7b8d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('interview_sessions', sa.Column('final_evaluation', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('interview_sessions', 'final_evaluation')
