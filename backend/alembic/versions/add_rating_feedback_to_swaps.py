"""
Add rating and feedback columns to swaps table

Revision ID: add_rating_feedback_to_swaps
Revises: add_message_to_swaps
Create Date: 2025-07-12 10:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_rating_feedback_to_swaps'
down_revision = 'add_message_to_swaps'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('swaps', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('swaps', sa.Column('feedback', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('swaps', 'rating')
    op.drop_column('swaps', 'feedback')
