"""update findings

Revision ID: f6d6ee4e1fcb
Revises: 4e818f3faf77
Create Date: 2021-04-11 03:08:08.436418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6d6ee4e1fcb'
down_revision = '4e818f3faf77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('findings', sa.Column('chrm', sa.String()))
    op.add_column('findings', sa.Column('start', sa.Integer))
    op.add_column('findings', sa.Column('end', sa.Integer))


def downgrade():
    op.drop_column('findings', 'chrm')
    op.drop_column('findings', 'start')
    op.drop_column('findings', 'end')
