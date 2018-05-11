"""empty message

Revision ID: fca9878e6bd8
Revises: 1aebf13af999
Create Date: 2018-04-21 22:04:03.971000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fca9878e6bd8'
down_revision = '1aebf13af999'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CarsDataset',
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('vehicleType', sa.Text(), nullable=True),
    sa.Column('yearOfRegistration', sa.Integer(), nullable=True),
    sa.Column('gearbox', sa.Text(), nullable=True),
    sa.Column('kilometer', sa.Integer(), nullable=True),
    sa.Column('brand', sa.Text(), nullable=True),
    sa.Column('lng', sa.FLOAT(), nullable=True),
    sa.Column('lat', sa.FLOAT(), nullable=True),
    sa.Column('seat', sa.Integer(), nullable=True),
    sa.Column('bluetooth', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Bdatetime', sa.Text(), nullable=True),
    sa.Column('Bday', sa.Text(), nullable=True),
    sa.Column('Btime', sa.Text(), nullable=True),
    sa.Column('Rdatetime', sa.Text(), nullable=True),
    sa.Column('Rday', sa.Text(), nullable=True),
    sa.Column('Rtime', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CarsDataset')
    # ### end Alembic commands ###
