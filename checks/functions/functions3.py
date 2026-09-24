# checks/functions/functions3.py
assert callable(double), "double should be a function"
assert double(3) == 6, "double(3) should return 6"
assert double(0) == 0, "double(0) should return 0"
assert double(-5) == -10, "double(-5) should return -10"
assert double(2.5) == 5.0, "double(2.5) should return 5.0"
print("functions3 ✓")
