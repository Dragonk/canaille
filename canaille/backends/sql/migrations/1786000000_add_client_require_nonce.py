"""Add per-client OIDC nonce requirement.

Legacy KMMS revision: kept in the chain so databases stamped by
the pre-rebase fork image (v0.3.6-kmms.x) can reach the new head.

Revision ID: 1786000000
Revises: 1785442300
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "1786000000"
down_revision: str | None = "1785442300"
branch_labels: str | Sequence[str] | None = ()
depends_on: str | Sequence[str] | None = None


def _has_column(table: str, column: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return column in {c["name"] for c in inspector.get_columns(table)}


def upgrade() -> None:
    """Add a nullable column so existing clients inherit the server default."""
    if not _has_column("client", "require_nonce"):
        op.add_column(
            "client", sa.Column("require_nonce", sa.Boolean(), nullable=True)
        )


def downgrade() -> None:
    if _has_column("client", "require_nonce"):
        op.drop_column("client", "require_nonce")
