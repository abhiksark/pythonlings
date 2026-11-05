from pathlib import Path

assert final == Path("reports/final.txt"), (
    f"final should be Path('reports/final.txt'), got {final!r}"
)
print("pathlib5 ok")
