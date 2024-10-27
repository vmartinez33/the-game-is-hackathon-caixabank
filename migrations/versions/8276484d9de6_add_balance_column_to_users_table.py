"""Add balance column to users table

Revision ID: 8276484d9de6
Revises: b55d97628019
Create Date: 2024-10-27 17:25:59.556230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8276484d9de6'
down_revision = 'b55d97628019'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Numeric(), nullable=False))
        batch_op.create_unique_constraint(None, ['phoneNumber'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('balance')

    # ### end Alembic commands ###
