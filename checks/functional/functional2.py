# checks/functional/functional2.py
assert absolute(5) == 5, f"absolute(5) should be 5, got {absolute(5)}"
assert absolute(-3) == 3, f"absolute(-3) should be 3, got {absolute(-3)}"
assert absolute(0) == 0, "absolute(0) should be 0"
assert absolute(-100) == 100, "absolute(-100) should be 100"
print("functional2 ✓")
