"""add changes for findings

Revision ID: 4e818f3faf77
Revises: 05104551cf13
Create Date: 2021-04-10 04:24:45.583488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e818f3faf77'
down_revision = '05104551cf13'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('findings',
    sa.Column('id', sa.Integer(), primary_key=True, index=True),
    sa.Column('workspace_id', sa.String()),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('gene', sa.String(), nullable=True),
    sa.Column('genes_in_view', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('chart_markers', sa.JSON, nullable=True)
    )


def downgrade():
    op.drop_table('findings')
