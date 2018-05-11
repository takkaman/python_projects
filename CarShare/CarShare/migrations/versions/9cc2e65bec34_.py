"""empty message

Revision ID: 9cc2e65bec34
Revises: 37b939dca8b5
Create Date: 2018-03-30 21:29:10.094000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cc2e65bec34'
down_revision = '37b939dca8b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('Bdatetime', sa.Text(), nullable=False),
    sa.Column('Bday', sa.Text(), nullable=False),
    sa.Column('Btime', sa.Text(), nullable=False),
    sa.Column('Rdatetime', sa.Text(), nullable=False),
    sa.Column('Rday', sa.Text(), nullable=False),
    sa.Column('Rtime', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('cattype', sa.String(length=100), nullable=False),
    sa.Column('gearbox', sa.String(length=100), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CarsDataset',
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('vehicleType', sa.Text(), nullable=False),
    sa.Column('yearOfRegistration', sa.Integer(), nullable=False),
    sa.Column('gearbox', sa.Text(), nullable=False),
    sa.Column('kilometer', sa.Integer(), nullable=False),
    sa.Column('brand', sa.Text(), nullable=False),
    sa.Column('lng', sa.Float(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CarsDataset')
    op.drop_table('Cars')
    # ### end Alembic commands ###
