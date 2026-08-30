from pathlib import Path


def test_oauth_schema_is_a_single_ldif_record():
    schema = Path("canaille/backends/ldap/schemas/oauth2-openldap.ldif").read_text()

    assert "\n\n" not in schema
