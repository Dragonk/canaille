"""Add per-client OIDC nonce requirement.

Revision ID: 1793481823
Revises: 1793118531
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "1793481823"
down_revision: str | None = "1793118531"
branch_labels: str | Sequence[str] | None = ()
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add a nullable column so existing clients inherit the server default."""
    op.add_column("client", sa.Column("require_nonce", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column("client", "require_nonce")
