"""empty message

Revision ID: 1067e628473c
Revises: ddb9f96ddad5
Create Date: 2022-05-13 10:50:36.082529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1067e628473c'
down_revision = 'ddb9f96ddad5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('netflix_titles', 'type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('netflix_titles', 'type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
