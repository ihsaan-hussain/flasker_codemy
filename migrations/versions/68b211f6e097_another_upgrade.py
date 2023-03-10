"""another upgrade

Revision ID: 68b211f6e097
Revises: ba6c9cb5abd0
Create Date: 2023-01-25 18:19:08.668443

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68b211f6e097'
down_revision = 'ba6c9cb5abd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_poseted', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_posted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posted', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('date_poseted')

    # ### end Alembic commands ###
