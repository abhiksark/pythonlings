from pathlib import Path

assert python_files == [Path("app.py"), Path("tests.py")], (
    f"python_files should be [Path('app.py'), Path('tests.py')], "
    f"got {python_files!r}"
)
print("pathlib4 ok")
