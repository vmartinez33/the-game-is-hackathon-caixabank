"""Add password reset columns to users table

Revision ID: e5478edcfd29
Revises: 6cd90922a03b
Create Date: 2024-10-27 22:04:59.216204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5478edcfd29'
down_revision = '6cd90922a03b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_reset_token', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('password_reset_token_expiration', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_reset_token_expiration')
        batch_op.drop_column('password_reset_token')

    # ### end Alembic commands ###
