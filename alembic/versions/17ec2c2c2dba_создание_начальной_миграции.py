"""Создание начальной миграции

Revision ID: 17ec2c2c2dba
Revises: 
Create Date: 2025-02-22 01:01:51.824188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17ec2c2c2dba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('pereval_images_pereval_id_fkey', 'pereval_images', type_='foreignkey')
    op.create_foreign_key(None, 'pereval_images', 'pereval_added', ['pereval_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pereval_images', type_='foreignkey')
    op.create_foreign_key('pereval_images_pereval_id_fkey', 'pereval_images', 'pereval_added', ['pereval_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
