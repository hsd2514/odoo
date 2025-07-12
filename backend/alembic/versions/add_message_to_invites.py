"""
Add message column to invites table

Revision ID: add_message_to_invites
Revises: 0197ad67d92c
Create Date: 2025-07-12 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_message_to_invites'
down_revision = '0197ad67d92c'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('invites', sa.Column('message', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('invites', 'message')
