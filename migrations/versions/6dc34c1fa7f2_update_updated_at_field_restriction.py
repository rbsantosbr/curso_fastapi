"""update updated_at field restriction

Revision ID: 6dc34c1fa7f2
Revises: 02d55705f9ee
Create Date: 2024-07-03 13:15:59.158266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc34c1fa7f2'
down_revision: Union[str, None] = '02d55705f9ee'
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
