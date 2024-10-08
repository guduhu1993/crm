"""更新表结构

Revision ID: c9075da4256f
Revises: cf758b191dbb
Create Date: 2024-08-30 14:56:57.894541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c9075da4256f'
down_revision: Union[str, None] = 'cf758b191dbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR USING role[1]")
    op.alter_column('users', 'role',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               type_=sa.Integer(),
               postgresql_using="role::integer",
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=sa.Integer(),
               type_=postgresql.ARRAY(sa.VARCHAR()),
               existing_nullable=True)
    # ### end Alembic commands ###
