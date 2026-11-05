from pathlib import Path

assert processed == Path("data/raw.json"), (
    f"processed should be Path('data/raw.json'), got {processed!r}"
)
assert parts[-2:] == ("data", "raw.json"), (
    f"parts[-2:] should be ('data', 'raw.json'), got {parts[-2:]!r}"
)
print("pathlib6 ok")
