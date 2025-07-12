"""Merge feedback/rating heads

Revision ID: ec37e2fff4a6
Revises: add_rating_feedback_to_invites, add_rating_feedback_to_swaps
Create Date: 2025-07-12 15:09:27.523439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec37e2fff4a6'
down_revision: Union[str, Sequence[str], None] = ('add_rating_feedback_to_invites', 'add_rating_feedback_to_swaps')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
