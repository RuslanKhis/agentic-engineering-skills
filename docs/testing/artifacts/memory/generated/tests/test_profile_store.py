import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

from profile_store import ProfileStore, UserScope


@pytest.mark.parametrize("language", ["English", "French", "Spanish", "Japanese"])
def test_save_replaces_and_survives_store_reconstruction(store, scope, language):
    assert store.get_preferred_language(scope) is None
    store.save_preferred_language(scope, "French", consent=True)
    store.save_preferred_language(scope, language, consent=True)
    store.save_preferred_language(scope, language, consent=True)
    reopened = ProfileStore(str(store.path))
    assert reopened.get_preferred_language(scope) == language


@pytest.mark.parametrize("consent", [False, None, 0, 1, "true"])
@pytest.mark.parametrize("existing", [None, "French"])
def test_only_explicit_true_consent_can_change_data(store, scope, consent, existing):
    if existing is not None:
        store.save_preferred_language(scope, existing, consent=True)
    with pytest.raises(PermissionError):
        store.save_preferred_language(scope, "Japanese", consent=consent)
    assert ProfileStore(store.path).get_preferred_language(scope) == existing


@pytest.mark.parametrize(
    "language",
    ["", " \t", "english", "FRENCH", "German", " French", "French\n", None, []],
)
def test_unsupported_language_does_not_change_data(store, scope, language):
    store.save_preferred_language(scope, "Spanish", consent=True)
    with pytest.raises(ValueError):
        store.save_preferred_language(scope, language, consent=True)
    assert ProfileStore(store.path).get_preferred_language(scope) == "Spanish"


@pytest.mark.parametrize("field", ["app_name", "user_id"])
@pytest.mark.parametrize("value", ["", " \t\n", None, 7])
@pytest.mark.parametrize("operation", ["save", "get", "forget"])
def test_invalid_scope_is_rejected_without_changes(store, scope, field, value, operation):
    store.save_preferred_language(scope, "French", consent=True)
    fields = {"app_name": scope.app_name, "user_id": scope.user_id}
    fields[field] = value
    invalid = UserScope(**fields)
    with pytest.raises(ValueError):
        if operation == "save":
            store.save_preferred_language(invalid, "Japanese", consent=True)
        elif operation == "get":
            store.get_preferred_language(invalid)
        else:
            store.forget_preferred_language(invalid)
    assert ProfileStore(store.path).get_preferred_language(scope) == "French"


def test_two_users_and_two_apps_can_forget_independently(store):
    scopes = [
        UserScope("app-one", "alice"),
        UserScope("app-one", "bob"),
        UserScope("app-two", "alice"),
        UserScope("app-two", "bob"),
    ]
    languages = ["English", "French", "Spanish", "Japanese"]
    for owner, language in zip(scopes, languages):
        store.save_preferred_language(owner, language, consent=True)
    for index, owner in enumerate(scopes):
        store.forget_preferred_language(owner)
        store.forget_preferred_language(owner)
        reopened = ProfileStore(store.path)
        for other_index, other in enumerate(scopes):
            expected = None if other_index <= index else languages[other_index]
            assert reopened.get_preferred_language(other) == expected


def test_identity_is_preserved_exactly_and_sql_is_parameterized(store):
    scopes = [
        UserScope("app", "alice"),
        UserScope(" app ", "alice"),
        UserScope("app", " alice "),
        UserScope("APP", "Alice"),
        UserScope("a:b", "c"),
        UserScope("a", "b:c"),
        UserScope("app'; DROP TABLE preferred_languages; --", "' OR 1=1 --"),
    ]
    for index, owner in enumerate(scopes):
        assert store.get_preferred_language(owner) is None
        store.save_preferred_language(
            owner, "French" if index % 2 else "Japanese", consent=True
        )
    for index, owner in enumerate(scopes):
        assert store.get_preferred_language(owner) == (
            "French" if index % 2 else "Japanese"
        )
    store.forget_preferred_language(scopes[-1])
    assert store.get_preferred_language(scopes[-1]) is None
    assert store.get_preferred_language(scopes[0]) == "Japanese"


def test_sqlite_failure_is_not_reported_as_missing_preference(store, scope):
    store.save_preferred_language(scope, "French", consent=True)
    # A damaged schema must surface as a storage failure, not an absent setting.
    with closing(sqlite3.connect(store.path)) as connection, connection:
        connection.execute("DROP TABLE preferred_languages")
    with pytest.raises(sqlite3.OperationalError):
        store.get_preferred_language(scope)
    with pytest.raises(sqlite3.OperationalError):
        store.save_preferred_language(scope, "Japanese", consent=True)
    with pytest.raises(sqlite3.OperationalError):
        store.forget_preferred_language(scope)


def test_persistence_and_forgetting_in_independent_processes(tmp_path):
    path = tmp_path / "process-profiles.sqlite3"
    # Child processes import only the local SQLite adapter and standard library.
    script = """
import sys
from profile_store import ProfileStore, UserScope
store = ProfileStore(sys.argv[1])
alice = UserScope('process-app', 'alice')
bob = UserScope('process-app', 'bob')
if sys.argv[2] == 'save':
    store.save_preferred_language(alice, 'French', consent=True)
    store.save_preferred_language(bob, 'Japanese', consent=True)
elif sys.argv[2] == 'read':
    assert store.get_preferred_language(alice) == 'French'
    assert store.get_preferred_language(bob) == 'Japanese'
elif sys.argv[2] == 'forget':
    store.forget_preferred_language(alice)
    store.forget_preferred_language(alice)
elif sys.argv[2] == 'verify':
    assert store.get_preferred_language(alice) is None
    assert store.get_preferred_language(bob) == 'Japanese'
"""
    for operation in ("save", "read", "forget", "verify"):
        result = subprocess.run(
            [sys.executable, "-B", "-c", script, str(path), operation],
            cwd=Path(__file__).resolve().parents[1],
            env={},
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0, result.stderr
