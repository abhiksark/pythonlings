from pathlib import Path

def test_pathlib4():
    python_files = [Path("app.py"), Path("tests.py")]
    assert python_files == [Path("app.py"), Path("tests.py")], "Expected python_files to be [Path('app.py'), Path('tests.py')]"

def test_pathlib5():
    final = Path("reports/final.txt")
    assert final == Path("reports/final.txt"), "Expected final to be Path('reports/final.txt')"

def test_pathlib6():
    processed = Path("data/raw.json")
    parts = processed.parts
    assert processed == Path("data/raw.json"), "Expected processed to be Path('data/raw.json')"
    assert parts[-2:] == ("data", "raw.json"), "Expected parts[-2:] to be ('data', 'raw.json')"
