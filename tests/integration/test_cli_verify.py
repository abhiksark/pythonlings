# tests/integration/test_cli_verify.py
import os
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures" / "tiny_curriculum"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args],
        capture_output=True,
        text=True,
    )


def _run_ascii(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI with stdout/stderr pinned to a strict ASCII encoding.

    Setting the encoding explicitly keeps the regression deterministic rather
    than depending on the locale the suite happens to run under.
    """
    env = {
        **os.environ,
        "PYTHONIOENCODING": "ascii",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
        "LC_ALL": "C",
        "LANG": "C",
    }
    return subprocess.run(
        [sys.executable, "-m", "pythonlings", *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_verify_fails_on_first_failure() -> None:
    # passing.py passes, asserts.py fails → verify exits non-zero.
    result = _run("--root", str(FIXTURES), "verify")
    assert result.returncode != 0
    assert "asserts" in (result.stdout + result.stderr)


def test_verify_against_only_passing_fixture(tmp_path: Path) -> None:
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "ok"\n'
        'path = "exercises/ok.py"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0, result.stderr


def test_verify_ignores_marker(tmp_path: Path) -> None:
    # An exercise with the marker still in place and checks passing
    # should be treated as a verify-pass.
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\nname = "ok"\npath = "exercises/ok.py"\nhint = "h"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text(
        "# I AM NOT DONE\nx = 1\n", encoding="utf-8"
    )
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert x == 1\n", encoding="utf-8")

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 0


def test_verify_reports_manifest_error_with_exit_2(tmp_path: Path) -> None:
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "info.toml" in result.stderr


def test_verify_malformed_toml_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text("format_version = [1\n", encoding="utf-8")
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "info.toml" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("pythonlings:")


def test_verify_invalid_utf8_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_bytes(b"\xff")
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "valid UTF-8" in result.stderr
    assert "Traceback" not in result.stderr


def test_verify_info_toml_read_error_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "info.toml").mkdir()
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "could not read info.toml" in result.stderr
    assert "Traceback" not in result.stderr


def test_verify_traversal_path_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "a"\n'
        'path = "exercises/../../etc/passwd"\n'
        'hint = "h"\n',
        encoding="utf-8",
    )
    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("pythonlings:")


def test_verify_directory_path_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "exercises" / "topic").mkdir(parents=True)
    (tmp_path / "checks" / "topic").mkdir(parents=True)
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "a"\n'
        'path = "exercises/topic"\n',
        encoding="utf-8",
    )

    result = _run("--root", str(tmp_path), "verify")
    assert result.returncode == 2
    assert "exercise path is not a file" in result.stderr
    assert "Traceback" not in result.stderr


def test_hint_non_string_field_exits_2_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "info.toml").write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "a"\n'
        'path = "exercises/a.py"\n'
        'hint = 1\n',
        encoding="utf-8",
    )

    result = _run("--root", str(tmp_path), "hint", "a")
    assert result.returncode == 2
    assert "hint" in result.stderr
    assert "Traceback" not in result.stderr


def test_verify_completes_under_ascii_encoding(tmp_path: Path) -> None:
    # A check prints "<name> ✓", so verify writes a non-ASCII glyph it captured
    # from the curriculum as well as its own status symbol. Neither may crash a
    # strict-ASCII console.
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "ok"\n'
        'path = "exercises/ok.py"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text("value = 1\n", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text(
        'assert value == 1, "value should be 1"\nprint("ok \u2713")\n',
        encoding="utf-8",
    )

    result = _run_ascii("--root", str(tmp_path), "verify")

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr
    assert "UnicodeEncodeError" not in result.stderr
    # The pass state stays visible through its ASCII stand-in.
    assert "+ ok" in result.stdout


def test_verify_keeps_unicode_symbol_under_utf8(tmp_path: Path) -> None:
    info = tmp_path / "info.toml"
    info.write_text(
        'format_version = 1\n'
        '[[exercises]]\n'
        'name = "ok"\n'
        'path = "exercises/ok.py"\n',
        encoding="utf-8",
    )
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "ok.py").write_text("value = 1\n", encoding="utf-8")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "ok.py").write_text("assert value == 1\n", encoding="utf-8")

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, "-m", "pythonlings", "--root", str(tmp_path), "verify"],
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "\u2713 ok" in result.stdout
