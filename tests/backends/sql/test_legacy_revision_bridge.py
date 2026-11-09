"""KMMS deployments stamped at legacy fork revision 1786000000 must reach head."""

def test_upgrade_from_legacy_1786000000(app, backend):
    """Simulate a DB left at the legacy fork revision, then bridge to head."""
    backend.alembic.downgrade("1785442300")
    backend.alembic.upgrade("1786000000")
    backend.alembic.upgrade()
