"""empty message

Revision ID: 8367df60a458
Revises: d960b75824ca
Create Date: 2020-05-17 14:22:03.284308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8367df60a458'
down_revision = 'd960b75824ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_active', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_active')
    # ### end Alembic commands ###
