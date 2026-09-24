from pathlib import Path

assert path == Path("notes/today.txt"), (
    f"path should be Path('notes/today.txt'), got {path!r}"
)
assert filename == "today.txt", (
    f"filename should be 'today.txt', got {filename!r}"
)
print("pathlib1 ok")
