"""added password field

Revision ID: 27def542704e
Revises: 442f0b11c7bb
Create Date: 2023-01-17 18:14:45.529337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27def542704e'
down_revision = '442f0b11c7bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
