"""empty message

Revision ID: 85c9c875d508
Revises: 7d1e9feceecb
Create Date: 2020-05-20 00:57:28.726796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c9c875d508'
down_revision = '7d1e9feceecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'profile', 'user', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'task', 'product', ['product_id'], ['id'])
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['id'])
    op.drop_column('task', 'size')
    op.add_column('user', sa.Column('proxies', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'proxies')
    op.add_column('task', sa.Column('size', sa.VARCHAR(length=10), nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'profile', type_='foreignkey')
    # ### end Alembic commands ###
