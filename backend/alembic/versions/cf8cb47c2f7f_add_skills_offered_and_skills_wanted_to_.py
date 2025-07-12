"""Add skills_offered and skills_wanted to users

Revision ID: cf8cb47c2f7f
Revises: ec37e2fff4a6
Create Date: 2025-07-12 16:06:06.738145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cf8cb47c2f7f'
down_revision: Union[str, Sequence[str], None] = 'ec37e2fff4a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Only add the new columns, do not drop or create any tables
    op.add_column('users', sa.Column('skills_offered', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('skills_wanted', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Only drop the new columns, do not drop or create any tables
    op.drop_column('users', 'skills_wanted')
    op.drop_column('users', 'skills_offered')
