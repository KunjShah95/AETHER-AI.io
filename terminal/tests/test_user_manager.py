import os
import json
import importlib.util
import sys


def _load_terminal_main():
    repo_root = os.getcwd()
    path = os.path.join(repo_root, 'terminal', 'main.py')
    spec = importlib.util.spec_from_file_location('terminal_main', path)
    module = importlib.util.module_from_spec(spec)
    # Insert lightweight mocks for heavy external dependencies to allow import during tests
    import types, sys
    # Create basic modules
    module_names = ['google', 'google.generativeai', 'groq', 'ollama', 'openai']
    for name in module_names:
        if name not in sys.modules:
            sys.modules[name] = types.ModuleType(name)

    # Provide a dummy Groq class for `from groq import Groq`
    if not hasattr(sys.modules['groq'], 'Groq'):
        class Groq:
            def __init__(self, *args, **kwargs):
                pass
        sys.modules['groq'].Groq = Groq
    spec.loader.exec_module(module)
    return module


def test_signup_and_login(tmp_path, monkeypatch):
    # Use a temporary HOME so USER_DB_PATH resolves into tmp
    monkeypatch.setenv('HOME', str(tmp_path))

    tm = _load_terminal_main()
    um = tm.UserManager()

    # Ensure no users initially
    assert um.list_users() == []

    ok, msg = um.signup('alice', 'password123')
    assert ok
    assert 'alice' in um.list_users()

    ok, msg = um.login('alice', 'password123')
    assert ok
    assert um.current_user == 'alice'


def test_legacy_sha256_migration(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))

    tm = _load_terminal_main()

    # Create a manual legacy user DB with sha256 hashed password
    import hashlib
    legacy_hash = hashlib.sha256('oldpass'.encode()).hexdigest()
    db = {'bob': {'password': legacy_hash, 'api_keys': {}, 'model': 'gemini', 'role': 'user'}}
    user_db_dir = tmp_path / '.nexus'
    user_db_dir.mkdir(parents=True, exist_ok=True)
    user_db_path = user_db_dir / 'users.json'
    with open(user_db_path, 'w') as f:
        json.dump(db, f)

    um = tm.UserManager()
    ok, msg = um.login('bob', 'oldpass')
    assert ok
    # After login, if passlib is installed we expect the password to be re-hashed
    try:
        from passlib.hash import bcrypt  # type: ignore
        passlib_present = True
    except Exception:
        passlib_present = False

    if passlib_present:
        assert um.user_db['bob']['password'] != legacy_hash
    else:
        # If passlib isn't available in the environment we fall back to sha256 and
        # the stored password will remain the legacy hash.
        assert um.user_db['bob']['password'] == legacy_hash