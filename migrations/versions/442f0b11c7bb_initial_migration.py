"""initial migration

Revision ID: 442f0b11c7bb
Revises: 
Create Date: 2023-01-13 18:36:06.691016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '442f0b11c7bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favourite_color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('favourite_color')

    # ### end Alembic commands ###
