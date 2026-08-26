from pathlib import Path

assert parent == Path("docs"), (
    f"parent should be Path('docs'), got {parent!r}"
)
assert stem == "guide", f"stem should be 'guide', got {stem!r}"
assert suffix == ".md", f"suffix should be '.md', got {suffix!r}"
print("pathlib3 ok")
