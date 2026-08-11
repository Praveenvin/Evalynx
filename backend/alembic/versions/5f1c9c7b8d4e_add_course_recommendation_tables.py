"""add course recommendation tables

Revision ID: 5f1c9c7b8d4e
Revises: d8e8d3cbfd83
Create Date: 2026-08-11 20:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f1c9c7b8d4e'
down_revision: Union[str, None] = 'd8e8d3cbfd83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('course_recommendations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('student_name', sa.String(), nullable=False),
    sa.Column('education', sa.String(), nullable=True),
    sa.Column('background', sa.String(), nullable=True),
    sa.Column('career_goal', sa.String(), nullable=False),
    sa.Column('current_skills', sa.JSON(), nullable=False),
    sa.Column('interests', sa.JSON(), nullable=False),
    sa.Column('summary', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommended_course_paths',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recommendation_id', sa.String(), nullable=False),
    sa.Column('step', sa.Integer(), nullable=False),
    sa.Column('course', sa.String(), nullable=False),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('difficulty', sa.String(), nullable=False),
    sa.Column('prerequisites', sa.JSON(), nullable=False),
    sa.Column('duration', sa.String(), nullable=False),
    sa.Column('skills_gained', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['recommendation_id'], ['course_recommendations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('recommended_course_paths')
    op.drop_table('course_recommendations')
