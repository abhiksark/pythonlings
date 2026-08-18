assert callable(double), "double should be a function"
assert double(3) == 6, f"double(3) should return 6, got {double(3)!r}"
assert double(0) == 0, f"double(0) should return 0, got {double(0)!r}"
assert double(-5) == -10, f"double(-5) should return -10, got {double(-5)!r}"
assert double(2.5) == 5.0, f"double(2.5) should return 5.0, got {double(2.5)!r}"
print("functions3 ✓")
