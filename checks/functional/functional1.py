# checks/functional/functional1.py
assert square(3) == 9, f"square(3) should be 9, got {square(3)}"
assert square(5) == 25, f"square(5) should be 25, got {square(5)}"
assert square(0) == 0, "square(0) should be 0"
print("functional1 ✓")
