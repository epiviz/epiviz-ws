"""drop the workspace_id string column

Revision ID: 05104551cf13
Revises: 2f35e03b8e04
Create Date: 2020-08-03 17:06:54.835265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05104551cf13'
down_revision = '2f35e03b8e04'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('workspaces', 'workspace_id')


def downgrade():
    op.add_column('workspaces',
        sa.Column('workspace_id', sa.String, index=True))
