"""Добавлена таблица PerevalLevel

Revision ID: 95042998aa7d
Revises: df8db8171dcd
Create Date: 2025-02-10 10:28:39.957616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95042998aa7d'
down_revision: Union[str, None] = 'df8db8171dcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
