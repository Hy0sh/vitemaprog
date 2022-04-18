"""Create Role

Revision ID: afaf471a233d
Revises: 7375613981f9
Create Date: 2022-04-18 15:23:37.637465

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'afaf471a233d'
down_revision = '7375613981f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('roles_rights',
    sa.Column('role_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('right_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['right_uuid'], ['rights.uuid'], ),
    sa.ForeignKeyConstraint(['role_uuid'], ['roles.uuid'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_rights')
    op.drop_table('roles')
    # ### end Alembic commands ###