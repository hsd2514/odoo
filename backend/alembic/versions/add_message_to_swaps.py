"""
Add message column to swaps table

Revision ID: add_message_to_swaps
Revises: add_created_at_to_invites
Create Date: 2025-07-12 10:15:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_message_to_swaps'
down_revision = 'add_created_at_to_invites'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('swaps', sa.Column('message', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('swaps', 'message')
