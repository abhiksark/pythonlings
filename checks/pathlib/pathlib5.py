from pathlib import Path

final = Path("reports/final.txt")
assert final == Path("reports/final.txt"), "Expected final to be Path('reports/final.txt')"
print("pathlib5 ok")