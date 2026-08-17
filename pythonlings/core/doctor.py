from __future__ import annotations

import errno
import json
import stat
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pythonlings.core.docs import load_snippet
from pythonlings.core.manifest import Manifest, ManifestError
from pythonlings.core.manifest import load as load_manifest
from pythonlings.core.state import FORMAT_VERSION


class CheckStatus(Enum):
    OK = "OK"
    WARNING = "WARN"
    FAILURE = "FAIL"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: CheckStatus
    message: str


@dataclass(frozen=True)
class DoctorReport:
    root: Path
    checks: tuple[CheckResult, ...]

    @property
    def has_failures(self) -> bool:
        return any(check.status is CheckStatus.FAILURE for check in self.checks)


def run_diagnostics(
    root: Path,
    *,
    package_version: str,
    resolution_error: Exception | None = None,
) -> DoctorReport:
    """Inspect an installation and workspace without modifying either."""
    display_root = root
    checks = [
        _check_runtime(),
        _check_package_version(package_version),
    ]
    if resolution_error is not None:
        checks.append(
            CheckResult(
                "Workspace",
                CheckStatus.FAILURE,
                f"could not resolve {display_root}: {resolution_error}; "
                "check the path and symlinks",
            )
        )
        return DoctorReport(root=display_root, checks=tuple(checks))
    try:
        display_root = root.expanduser()
        root = display_root.resolve()
    except (OSError, RuntimeError) as exc:
        checks.append(
            CheckResult(
                "Workspace",
                CheckStatus.FAILURE,
                f"could not resolve {display_root}: {exc}; check the path and symlinks",
            )
        )
        return DoctorReport(root=display_root, checks=tuple(checks))

    checks.append(_check_workspace(root))

    manifest_result, manifest = _check_manifest(root)
    checks.append(manifest_result)
    checks.extend(
        [
            _check_solutions(root, manifest),
            _check_state(root),
            _check_originals(root, manifest),
            _check_docs(manifest),
        ]
    )
    return DoctorReport(root=root, checks=tuple(checks))


def _check_runtime() -> CheckResult:
    version = ".".join(str(part) for part in sys.version_info[:3])
    if sys.version_info < (3, 9):
        return CheckResult(
            "Python runtime",
            CheckStatus.FAILURE,
            f"Python {version} is unsupported; Python 3.9+ is required",
        )
    return CheckResult("Python runtime", CheckStatus.OK, f"Python {version}")


def _check_package_version(package_version: str) -> CheckResult:
    if package_version == "0.0.0+unknown":
        return CheckResult(
            "Pythonlings version",
            CheckStatus.WARNING,
            "package metadata is unavailable (source checkout)",
        )
    return CheckResult(
        "Pythonlings version", CheckStatus.OK, f"pythonlings {package_version}"
    )


def _check_workspace(root: Path) -> CheckResult:
    try:
        mode = root.stat().st_mode
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            return CheckResult(
                "Workspace",
                CheckStatus.FAILURE,
                f"{root} is a symlink loop; check the path and symlinks",
            )
        if exc.errno in (errno.ENOENT, errno.ENOTDIR):
            return CheckResult(
                "Workspace",
                CheckStatus.FAILURE,
                f"{root} does not exist; run `pythonlings init --path {root}`",
            )
        raise
    if not stat.S_ISDIR(mode):
        return CheckResult(
            "Workspace", CheckStatus.FAILURE, f"{root} is not a directory"
        )

    invalid: list[str] = []
    if not (root / "info.toml").is_file():
        invalid.append("info.toml (file)")
    for dirname in ("exercises", "checks"):
        if not (root / dirname).is_dir():
            invalid.append(f"{dirname}/ (directory)")
    if invalid:
        return CheckResult(
            "Workspace",
            CheckStatus.FAILURE,
            f"missing or invalid required paths: {', '.join(invalid)}; "
            "run `pythonlings update --path <workspace>` or initialize a new workspace",
        )
    return CheckResult("Workspace", CheckStatus.OK, str(root))


def _check_manifest(root: Path) -> tuple[CheckResult, Manifest | None]:
    try:
        manifest = load_manifest(root)
    except (
        ManifestError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
    ) as exc:
        return (
            CheckResult(
                "Manifest",
                CheckStatus.FAILURE,
                f"{exc}; fix info.toml or run "
                "`pythonlings update --path <workspace>`",
            ),
            None,
        )

    validation_error = _manifest_validation_error(manifest)
    if validation_error is not None:
        return (
            CheckResult(
                "Manifest",
                CheckStatus.FAILURE,
                f"{validation_error}; fix info.toml or run "
                "`pythonlings update --path <workspace>`",
            ),
            None,
        )
    return (
        CheckResult(
            "Manifest",
            CheckStatus.OK,
            f"{len(manifest.exercises)} exercises across "
            f"{len(manifest.topics())} topics",
        ),
        manifest,
    )


def _check_solutions(root: Path, manifest: Manifest | None) -> CheckResult:
    solutions = root / "solutions"
    if manifest is None:
        message = (
            "directory is missing and coverage could not be checked"
            if not solutions.is_dir()
            else "coverage could not be checked because the manifest is invalid"
        )
        return CheckResult("Solutions", CheckStatus.WARNING, message)

    missing = [
        exercise.name
        for exercise in manifest.exercises
        if not (solutions / f"{exercise.name}.py").is_file()
    ]
    if missing:
        return CheckResult(
            "Solutions",
            CheckStatus.WARNING,
            _missing_message(missing, len(manifest.exercises))
            + "; run `pythonlings update --path <workspace>`",
        )
    return CheckResult(
        "Solutions",
        CheckStatus.OK,
        f"{len(manifest.exercises)}/{len(manifest.exercises)} available",
    )


def _check_state(root: Path) -> CheckResult:
    path = root / ".pythonlings" / "state.json"
    if path.is_symlink():
        try:
            path.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            return CheckResult(
                "Progress state",
                CheckStatus.WARNING,
                f"state.json is a broken symlink: {exc}; replace or remove the link",
            )
    if not path.exists():
        return CheckResult("Progress state", CheckStatus.OK, "no progress file yet")
    if not path.is_file():
        return CheckResult(
            "Progress state",
            CheckStatus.WARNING,
            f"{path} is not a regular file; replace it with a valid state.json",
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return CheckResult(
            "Progress state",
            CheckStatus.WARNING,
            f"state.json is unreadable: {exc}; back it up before starting Pythonlings",
        )

    if not isinstance(data, dict):
        return CheckResult(
            "Progress state",
            CheckStatus.WARNING,
            "state.json must contain an object; back it up before starting Pythonlings",
        )
    if data.get("format_version") != FORMAT_VERSION:
        return CheckResult(
            "Progress state",
            CheckStatus.WARNING,
            "unsupported format_version "
            f"{data.get('format_version')!r}; expected {FORMAT_VERSION}; "
            "back it up before starting Pythonlings",
        )
    completed = data.get("completed", [])
    if not isinstance(completed, list) or not all(
        isinstance(name, str) for name in completed
    ):
        return CheckResult(
            "Progress state",
            CheckStatus.WARNING,
            "completed must be a list of exercise names; "
            "back up state.json before starting Pythonlings",
        )
    return CheckResult(
        "Progress state", CheckStatus.OK, f"readable ({len(completed)} completed)"
    )


def _check_originals(root: Path, manifest: Manifest | None) -> CheckResult:
    originals = root / ".pythonlings" / "originals"
    if manifest is None:
        message = (
            "directory is missing and coverage could not be checked"
            if not originals.is_dir()
            else "coverage could not be checked because the manifest is invalid"
        )
        return CheckResult("Reset snapshots", CheckStatus.WARNING, message)

    missing: list[str] = []
    for exercise in manifest.exercises:
        if exercise.rel_path is None:
            original = originals / f"{exercise.name}.py"
        else:
            original = originals / exercise.rel_path.relative_to("exercises")
        if not original.is_file():
            missing.append(exercise.name)

    if missing:
        return CheckResult(
            "Reset snapshots",
            CheckStatus.WARNING,
            _missing_message(missing, len(manifest.exercises))
            + "; run `pythonlings update --path <workspace>`",
        )
    return CheckResult(
        "Reset snapshots",
        CheckStatus.OK,
        f"{len(manifest.exercises)}/{len(manifest.exercises)} available",
    )


def _check_docs(manifest: Manifest | None) -> CheckResult:
    try:
        if manifest is None:
            snippet = load_snippet("variables")
            if snippet is None:
                return CheckResult(
                    "Bundled docs",
                    CheckStatus.WARNING,
                    "documentation is unavailable; reinstall pythonlings",
                )
            return CheckResult(
                "Bundled docs",
                CheckStatus.OK,
                "documentation index is readable; topic coverage was not checked",
            )

        missing: list[str] = []
        topics = manifest.topics()
        for topic in topics:
            exercise = manifest.exercises_in(topic)[0]
            if load_snippet(topic, exercise.docs) is None:
                missing.append(topic)
    except (
        OSError,
        UnicodeError,
        KeyError,
        TypeError,
        AttributeError,
        ValueError,
    ) as exc:
        return CheckResult(
            "Bundled docs",
            CheckStatus.WARNING,
            f"documentation is unreadable: {exc}; reinstall pythonlings",
        )
    if missing:
        return CheckResult(
            "Bundled docs",
            CheckStatus.WARNING,
            _missing_message(missing, len(topics)) + "; reinstall pythonlings",
        )
    return CheckResult(
        "Bundled docs",
        CheckStatus.OK,
        f"{len(topics)}/{len(topics)} topics available",
    )


def _missing_message(missing: list[str], total: int) -> str:
    shown = ", ".join(str(item) for item in missing[:3])
    if len(missing) > 3:
        shown += ", ..."
    return f"{len(missing)}/{total} missing ({shown})"


def _manifest_validation_error(manifest: Manifest) -> str | None:
    if not isinstance(manifest.welcome_message, str):
        return "welcome_message must be a string"
    if not isinstance(manifest.final_message, str):
        return "final_message must be a string"

    for exercise in manifest.exercises:
        if not isinstance(exercise.name, str) or not exercise.name:
            return f"exercise name must be a non-empty string, got {exercise.name!r}"
        if not isinstance(exercise.hint, str):
            return f"hint for {exercise.name!r} must be a string"
        if not isinstance(exercise.docs, str):
            return f"docs for {exercise.name!r} must be a string"
        if not exercise.path.is_file():
            return f"exercise path is not a file: {exercise.rel_path or exercise.path}"
        if not exercise.check_path.is_file():
            return (
                "check path is not a file: "
                f"{exercise.check_rel_path or exercise.check_path}"
            )
    return None
