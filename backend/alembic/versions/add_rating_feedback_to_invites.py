"""
Add rating and feedback columns to invites table

Revision ID: add_rating_feedback_to_invites
Revises: add_created_at_to_invites
Create Date: 2025-07-12 10:35:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_rating_feedback_to_invites'
down_revision = 'add_created_at_to_invites'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('invites', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('invites', sa.Column('feedback', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('invites', 'rating')
    op.drop_column('invites', 'feedback')
