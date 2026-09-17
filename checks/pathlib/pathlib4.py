from pathlib import Path

python_files = [Path("app.py"), Path("tests.py")]
assert python_files == [Path("app.py"), Path("tests.py")], "Expected python_files to be [Path('app.py'), Path('tests.py')]"
print("pathlib4 ok")