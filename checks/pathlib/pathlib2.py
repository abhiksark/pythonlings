from pathlib import Path

assert source == Path("pythonlings/src/main.py"), (
    f"source should be Path('pythonlings/src/main.py'), got {source!r}"
)
print("pathlib2 ok")
