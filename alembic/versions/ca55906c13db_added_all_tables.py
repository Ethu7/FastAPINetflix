"""Added all tables

Revision ID: ca55906c13db
Revises: c6afd4f4a971
Create Date: 2022-05-12 14:16:38.020471

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca55906c13db'
down_revision = 'c6afd4f4a971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('netflix_titles', sa.Column('show_id', sa.String(), nullable=False))
    op.add_column('netflix_titles', sa.Column('type', sa.String(), nullable=False))
    op.add_column('netflix_titles', sa.Column('title', sa.String(), nullable=False))
    op.add_column('netflix_titles', sa.Column('director', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('cast', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('country', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('date_added', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('release_year', sa.Integer(), nullable=False))
    op.add_column('netflix_titles', sa.Column('rating', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('duration', sa.String(), nullable=True))
    op.add_column('netflix_titles', sa.Column('listed_in', sa.String(), nullable=False))
    op.add_column('netflix_titles', sa.Column('description', sa.String(), nullable=False))
    op.add_column('netflix_titles', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'netflix_titles', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'netflix_titles', type_='foreignkey')
    op.drop_column('netflix_titles', 'owner_id')
    op.drop_column('netflix_titles', 'description')
    op.drop_column('netflix_titles', 'listed_in')
    op.drop_column('netflix_titles', 'duration')
    op.drop_column('netflix_titles', 'rating')
    op.drop_column('netflix_titles', 'release_year')
    op.drop_column('netflix_titles', 'date_added')
    op.drop_column('netflix_titles', 'country')
    op.drop_column('netflix_titles', 'cast')
    op.drop_column('netflix_titles', 'director')
    op.drop_column('netflix_titles', 'title')
    op.drop_column('netflix_titles', 'type')
    op.drop_column('netflix_titles', 'show_id')
    op.drop_table('votes')
    op.drop_table('posts')
    # ### end Alembic commands ###
