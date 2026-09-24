# checks/json/json8.py
assert decoded == original, f"Expected decoded dict to equal original {original!r}, got {decoded!r}"
assert tag_count == 2, f"Expected tag_count to be 2, got {tag_count!r}"
assert level == 3, f"Expected level to be 3, got {level!r}"
print("json8 ok")
