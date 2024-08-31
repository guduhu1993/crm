"""create account table

Revision ID: d5ddf5ac4deb
Revises: c9075da4256f
Create Date: 2024-08-30 16:01:24.783840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5ddf5ac4deb'
down_revision: Union[str, None] = 'c9075da4256f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
