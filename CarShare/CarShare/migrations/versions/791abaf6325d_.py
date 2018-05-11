"""empty message

Revision ID: 791abaf6325d
Revises: 3ab52d12dfbd
Create Date: 2018-04-04 13:02:29.207000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '791abaf6325d'
down_revision = '3ab52d12dfbd'
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
    sa.Column('lng', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Integer(), nullable=False),
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
