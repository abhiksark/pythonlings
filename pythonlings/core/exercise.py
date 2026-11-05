# pythonlings/core/exercise.py
from __future__ import annotations

import io
import tokenize
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Exercise:
    name: str
    path: Path
    check_path: Path
    topic: str
    hint: str
    docs: str = ""
    root: Path | None = None
    rel_path: Path | None = None
    check_rel_path: Path | None = None

    DONE_MARKER = "# I AM NOT DONE"

    def is_pending(self) -> bool:
        return self.DONE_MARKER in self.path.read_text(encoding="utf-8")

    def strip_marker(self, text: str) -> str:
        """Remove standalone marker comments while preserving program text."""
        # Token rows count newlines, not Unicode separators inside strings.
        lines = io.StringIO(text).readlines()
        try:
            markers = {
                token.start[0]
                for token in tokenize.generate_tokens(
                    io.StringIO(text).readline
                )
                if token.type == tokenize.COMMENT
                and token.string.strip() == self.DONE_MARKER
                and lines[token.start[0] - 1].strip() == self.DONE_MARKER
            }
        except (tokenize.TokenError, IndentationError):
            return text
        return "".join(
            line
            for number, line in enumerate(lines, 1)
            if number not in markers
        )


@dataclass
class RunResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool
