"""merge bitacora y reportes

Revision ID: 68bf88586e58
Revises: 5ea595e82268, aa12e39f65e0
Create Date: 2026-04-26 15:19:46.408124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68bf88586e58'
down_revision: Union[str, Sequence[str], None] = ('5ea595e82268', 'aa12e39f65e0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
