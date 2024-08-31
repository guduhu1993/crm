"""更新表结构

Revision ID: cf758b191dbb
Revises: 5d8ee24aef93
Create Date: 2024-08-30 13:55:57.741084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf758b191dbb'
down_revision: Union[str, None] = '5d8ee24aef93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('role_label', sa.String(), nullable=True))
    op.add_column('roles', sa.Column('status', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('privileges', sa.String(), nullable=True))
    op.drop_index('ix_roles_title', table_name='roles')
    op.create_index(op.f('ix_roles_role_label'), 'roles', ['role_label'], unique=True)
    op.drop_column('roles', 'options')
    op.drop_column('roles', 'title')
    op.drop_column('roles', 'statu')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('statu', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('roles', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('roles', sa.Column('options', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_roles_role_label'), table_name='roles')
    op.create_index('ix_roles_title', 'roles', ['title'], unique=True)
    op.drop_column('roles', 'privileges')
    op.drop_column('roles', 'status')
    op.drop_column('roles', 'role_label')
    # ### end Alembic commands ###
