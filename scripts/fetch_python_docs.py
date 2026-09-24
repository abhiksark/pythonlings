#!/usr/bin/env python3
"""Fetch small local reference snippets from the official Python docs.

The generated snippets are committed so learners can use pythonlings offline.
Run from the repository root:

    python scripts/fetch_python_docs.py
"""

from __future__ import annotations

import argparse
import html
import json
import textwrap
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag


BASE_URL = "https://docs.python.org/3/"
OUTPUT = Path("pythonlings/docs")
MAX_LINES = 40


@dataclass(frozen=True)
class Source:
    topic: str
    title: str
    url: str
    summary: str
    extra_url: str = ""
    extra_summary: str = ""


SOURCES: tuple[Source, ...] = (
    Source("variables", "Variables", BASE_URL + "tutorial/introduction.html#using-python-as-a-calculator", "Assigning names with `=` lets you keep values for later expressions.", BASE_URL + "reference/simple_stmts.html#assignment-statements", "Assignment statement syntax and semantics, including multiple and unpacking targets."),
    Source("strings", "Strings", BASE_URL + "library/stdtypes.html#text-sequence-type-str", "Strings are immutable text sequences with indexing, slicing, and many useful methods.", BASE_URL + "library/stdtypes.html#string-methods", "Full reference of string methods with signatures and behaviors."),
    Source("conditionals", "Conditionals", BASE_URL + "tutorial/controlflow.html#if-statements", "`if`, `elif`, and `else` choose which block runs based on boolean conditions.", BASE_URL + "tutorial/controlflow.html#match-statements", "`match` pattern matching with examples and syntax."),
    Source("loops", "Loops", BASE_URL + "tutorial/controlflow.html#for-statements", "`for` loops iterate over items; `while` loops continue while a condition is true.", BASE_URL + "reference/compound_stmts.html#the-for-statement", "Formal for-statement syntax and iteration semantics."),
    Source("functions", "Functions", BASE_URL + "tutorial/controlflow.html#defining-functions", "`def` creates reusable behavior with parameters, return values, and optional defaults.", BASE_URL + "reference/compound_stmts.html#function-definitions", "Function definition syntax including parameters, annotations, and decorators."),
    Source("lists", "Lists", BASE_URL + "tutorial/datastructures.html#more-on-lists", "Lists are mutable ordered collections with methods such as `append`, `pop`, and `sort`.", BASE_URL + "library/stdtypes.html#sequence-types-list-tuple-range", "Sequence types reference with list methods, operations, and type tables."),
    Source("tuples", "Tuples", BASE_URL + "tutorial/datastructures.html#tuples-and-sequences", "Tuples group ordered values and are commonly unpacked into multiple names.", BASE_URL + "library/stdtypes.html#common-sequence-operations", "Operations shared by all sequence types: indexing, slicing, concatenation."),
    Source("dictionaries", "Dictionaries", BASE_URL + "tutorial/datastructures.html#dictionaries", "Dictionaries map keys to values and are the standard way to represent lookup tables.", BASE_URL + "library/stdtypes.html#mapping-types-dict", "The dict type with constructor forms, methods, and creation examples."),
    Source("sets", "Sets", BASE_URL + "tutorial/datastructures.html#sets", "Sets store unique values and support membership tests and set operations.", BASE_URL + "library/stdtypes.html#set-types-set-frozenset", "set and frozenset methods for membership and set relationships."),
    Source("comprehensions", "Comprehensions", BASE_URL + "tutorial/datastructures.html#list-comprehensions", "Comprehensions build new collections by combining an expression with one or more loops.", BASE_URL + "tutorial/datastructures.html#nested-list-comprehensions", "Nested comprehensions that build lists of lists from multiple loops."),
    Source("exceptions", "Exceptions", BASE_URL + "tutorial/errors.html#handling-exceptions", "`try` and `except` handle errors without crashing the whole program.", BASE_URL + "library/exceptions.html#concrete-exceptions", "Concrete built-in exceptions like ValueError, KeyError, and TypeError."),
    Source("file_io", "File I/O", BASE_URL + "tutorial/inputoutput.html#reading-and-writing-files", "`open` and `with` are the usual tools for reading and writing files safely.", BASE_URL + "library/io.html#high-level-module-interface", "The high-level `open()` interface and its modes."),
    Source("classes", "Classes", BASE_URL + "tutorial/classes.html#a-first-look-at-classes", "Classes combine data and behavior into reusable types.", BASE_URL + "reference/datamodel.html#special-method-names", "Special methods like `__init__`, `__str__`, and `__repr__`."),
    Source("functional", "Functional Tools", BASE_URL + "howto/functional.html", "Functional style uses functions, iterators, and transformations as building blocks.", BASE_URL + "library/itertools.html#itertool-functions", "itertools building blocks with signatures and usage patterns."),
    Source("decorators", "Decorators", BASE_URL + "reference/compound_stmts.html#function-definitions", "Decorators wrap or transform functions and classes with `@decorator` syntax.", BASE_URL + "library/functools.html#functools.wraps", "`functools.wraps` preserves the wrapped function's metadata."),
    Source("generators", "Generators", BASE_URL + "tutorial/classes.html#generators", "Generators produce values lazily with `yield` instead of returning a whole collection.", BASE_URL + "reference/expressions.html#generator-expressions", "Generator expression syntax for compact lazy iterators."),
    Source("context_managers", "Context Managers", BASE_URL + "reference/compound_stmts.html#the-with-statement", "Context managers run setup and cleanup around a block using `with`.", BASE_URL + "library/contextlib.html#contextlib.contextmanager", "`contextlib.contextmanager` builds a context manager from a generator."),
    Source("dataclasses", "Dataclasses", BASE_URL + "library/dataclasses.html", "Dataclasses generate common class methods for data-focused classes.", BASE_URL + "tutorial/classes.html#class-and-instance-variables", "Class vs instance variables — the distinction behind dataclass fields."),
    Source("type_hints", "Type Hints", BASE_URL + "library/typing.html", "Type hints annotate expected values and help tools reason about your code.", BASE_URL + "reference/datamodel.html#annotations", "How annotations are stored in `__annotations__`."),
    Source("regex", "Regular Expressions", BASE_URL + "library/re.html", "The `re` module searches, matches, and transforms text using regular expressions.", BASE_URL + "howto/regex.html#search-and-replace", "Practical search-and-replace patterns from the regex HOWTO."),
    Source("testing", "Testing", BASE_URL + "library/unittest.html", "Tests encode expected behavior so code can be checked repeatedly.", BASE_URL + "library/doctest.html#how-it-works", "How doctest finds and runs examples embedded in docstrings."),
    Source("recursion", "Recursion", BASE_URL + "tutorial/controlflow.html#defining-functions", "Recursive functions solve a problem by calling themselves on smaller inputs.", BASE_URL + "library/sys.html#sys.setrecursionlimit", "Adjusting the interpreter's recursion limit with `sys.setrecursionlimit`."),
    Source("modules", "Modules", BASE_URL + "tutorial/modules.html#modules", "Modules organize Python code into importable files and packages.", BASE_URL + "library/importlib.html#importlib.reload", "Reloading and dynamically importing modules with importlib."),
    Source("collections", "Collections", BASE_URL + "library/collections.html", "`collections` provides specialized containers beyond the built-in list, dict, set, and tuple.", BASE_URL + "library/collections.html#collections.Counter", "`Counter` tallies hashable objects and finds the most common ones."),
    Source("itertools", "Itertools", BASE_URL + "library/itertools.html", "`itertools` provides fast iterator building blocks for loops and data pipelines.", BASE_URL + "howto/functional.html#the-itertools-module", "The functional HOWTO's tour of itertools with examples."),
    Source("json", "JSON", BASE_URL + "library/json.html", "`json` converts between Python values and JSON text.", BASE_URL + "tutorial/inputoutput.html#saving-structured-data-with-json", "Tutorial on saving and loading structured data as JSON."),
    Source("datetime", "Datetime", BASE_URL + "library/datetime.html", "`datetime` represents dates, times, durations, and time zones.", BASE_URL + "library/datetime.html#examples-of-usage-datetime", "Worked `datetime` examples beyond the API reference."),
    Source("enums", "Enums", BASE_URL + "library/enum.html", "Enums define named constant values that are easier to read than raw literals.", BASE_URL + "library/enum.html#enum.Flag", "`Flag` enums combine members with bitwise operators."),
    Source("pathlib", "Pathlib", BASE_URL + "library/pathlib.html", "`pathlib.Path` represents filesystem paths with object-oriented helpers.", BASE_URL + "library/pathlib.html#pathlib.Path.mkdir", "`Path.mkdir` creates directories with parents/exist_ok options."),
    Source("oop_advanced", "Advanced OOP", BASE_URL + "tutorial/classes.html", "Advanced class patterns build on attributes, methods, inheritance, and special methods.", BASE_URL + "reference/datamodel.html#object.__repr__", "`__repr__` and `__str__` for custom object representations."),
    Source("async", "Asyncio", BASE_URL + "library/asyncio.html", "`asyncio` runs concurrent I/O-bound work with coroutines and an event loop.", BASE_URL + "library/asyncio-task.html#coroutines", "Coroutines and `async`/`await` with execution examples."),
)


class SectionParser(HTMLParser):
    """Extract the text of the element bearing a target id (or the whole body).

    Triggers on any element whose id matches the URL fragment. A `<section>`
    anchor captures that section; a `<dt>` anchor (Sphinx object/method entry)
    captures its enclosing `<dl>` so the signature and description come together.
    """

    def __init__(self, target_id: str | None) -> None:
        super().__init__(convert_charrefs=True)
        self.target_id = target_id
        self.capture = target_id is None
        self.found = target_id is None
        self.depth = 0
        self.capture_tag: str | None = None
        self.dl_depth = 0
        self.skip_depth = 0
        self.in_pre = False
        self.in_code = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in {"script", "style", "nav", "footer"}:
            self.skip_depth += 1
            return

        if tag == "dl":
            self.dl_depth += 1

        if (
            not self.capture
            and self.target_id is not None
            and attr.get("id") == self.target_id
        ):
            self.capture = True
            self.found = True
            # A <dt> is just a signature; capture the enclosing <dl> instead so
            # the description (<dd>) is included.
            self.capture_tag = "dl" if (tag == "dt" and self.dl_depth) else tag
            self.depth = 1
        elif self.capture and tag == self.capture_tag:
            self.depth += 1

        if not self._collecting():
            return

        if tag in {"h1", "h2", "h3"}:
            self.parts.append("\n\n")
        elif tag == "p":
            self.parts.append("\n\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "pre":
            self.in_pre = True
            self.parts.append("\n\n```python\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.parts.append("`")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer"} and self.skip_depth:
            self.skip_depth -= 1
            return

        if self._collecting():
            if tag in {"p", "li"}:
                self.parts.append("\n")
            elif tag == "pre":
                self.in_pre = False
                self.parts.append("\n```\n")
            elif tag == "code" and self.in_code:
                self.in_code = False
                self.parts.append("`")

        if self.capture and tag == self.capture_tag and self.depth:
            self.depth -= 1
            if self.depth == 0:
                self.capture = False

        if tag == "dl":
            self.dl_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._collecting():
            self.parts.append(data)

    def _collecting(self) -> bool:
        return self.capture and self.skip_depth == 0


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "pythonlings-doc-fetcher/0.1"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def extract(html_text: str, url: str) -> str:
    _, anchor = urldefrag(url)
    parser = SectionParser(anchor or None)
    parser.feed(html_text)
    text = html.unescape("".join(parser.parts))
    lines = normalize_lines(text)
    if not parser.found or not lines:
        raise RuntimeError(f"could not extract docs section from {url}")
    return "\n".join(lines[:MAX_LINES]).strip()


def normalize_lines(text: str) -> list[str]:
    lines: list[str] = []
    blank = False
    for raw in text.splitlines():
        line = " ".join(raw.strip().replace("¶", "").split())
        if not line:
            if lines and not blank:
                lines.append("")
            blank = True
            continue
        lines.append(line)
        blank = False
    while lines and not lines[-1]:
        lines.pop()
    return lines


def render_markdown(source: Source, extracted: str, extra: str = "") -> str:
    md = (
        f"# {source.title}\n\n"
        f"Source: {source.url}\n\n"
        "This local reference is generated from the official Python documentation "
        "and trimmed for pythonlings.\n\n"
        f"{source.summary}\n\n"
        "## Extracted reference\n\n"
        f"{extracted}\n"
    )
    if extra:
        md += (
            "\n## More reference\n\n"
            f"Source: {source.extra_url}\n\n"
            f"{source.extra_summary}\n\n"
            f"{extra}\n"
        )
    return md


def write_outputs(sources: tuple[Source, ...], output: Path) -> None:
    topics_dir = output / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)
    index = {"generated_from": BASE_URL, "topics": {}}

    for source in sources:
        print(f"fetch {source.topic}: {source.url}")
        extracted = extract(fetch(source.url), source.url)
        extra = ""
        if source.extra_url:
            try:
                extra = extract(fetch(source.extra_url), source.extra_url)
            except Exception as e:  # noqa: BLE001 — extra section is best-effort
                print(f"  warn: skipped extra for {source.topic}: {e}")
        filename = f"topics/{source.topic}.md"
        (output / filename).write_text(
            render_markdown(source, extracted, extra), encoding="utf-8"
        )
        index["topics"][source.topic] = {
            "title": source.title,
            "source_url": source.url,
            "file": filename,
        }

    (output / "index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "NOTICE.md").write_text(
        textwrap.dedent(
            """\
            # Bundled Python Documentation Snippets

            These snippets are generated from the official Python documentation at
            https://docs.python.org/3/ and trimmed for use inside pythonlings.

            Python documentation pages are licensed under the Python Software
            Foundation License Version 2. Examples, recipes, and other code in the
            documentation are additionally licensed under the Zero Clause BSD License.
            See https://docs.python.org/3/copyright.html for details.
            """
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    write_outputs(SOURCES, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
