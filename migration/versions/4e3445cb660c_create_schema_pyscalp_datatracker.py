"""create schema pyscalp datatracker

Revision ID: 4e3445cb660c
Revises: 
Create Date: 2025-01-14 21:45:56.710729

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '4e3445cb660c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS pyscalp_datatracker;')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS pyscalp_datatracker CASCADE;')

