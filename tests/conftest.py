from __future__ import annotations

import pytest


@pytest.fixture(autouse=True, scope="function")
def _isolate_pythonlings_home(monkeypatch, tmp_path):
    """Point PYTHONLINGS_HOME at a fresh tmp dir for every test.

    This prevents any test from accidentally creating or reading the
    developer's real ~/.pythonlings workspace.

    Tests that need to exercise the *absence* of PYTHONLINGS_HOME
    (e.g. test_default_root_falls_back_to_hidden_home_dir) can simply
    call ``monkeypatch.delenv("PYTHONLINGS_HOME", raising=False)`` in
    their own body — the per-test monkeypatch runs after this fixture
    but within the same scope, so the test's own delenv/setenv wins.
    """
    monkeypatch.setenv("PYTHONLINGS_HOME", str(tmp_path / "_pythonlings_home"))
