from pathlib import Path

processed = Path("data/raw.json")
parts = processed.parts
assert processed == Path("data/raw.json"), "Expected processed to be Path('data/raw.json')"
assert parts[-2:] == ("data", "raw.json"), "Expected parts[-2:] to be ('data', 'raw.json')"
print("pathlib6 ok")