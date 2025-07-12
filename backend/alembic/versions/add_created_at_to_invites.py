"""
Add created_at column to invites table

Revision ID: add_created_at_to_invites
Revises: add_message_to_invites
Create Date: 2025-07-12 10:10:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_created_at_to_invites'
down_revision = 'add_message_to_invites'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('invites', sa.Column('created_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('invites', 'created_at')
