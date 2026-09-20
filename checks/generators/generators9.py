# generators9.py
assert list(Counter(4)) == [0, 1, 2, 3], "Expected list(Counter(4)) to be [0, 1, 2, 3]"
assert list(Counter(1)) == [0], "Expected list(Counter(1)) to be [0]"
assert list(Counter(0)) == [], "Expected list(Counter(0)) to be [] (no elements when stop is 0)"
c = Counter(2)
assert next(c) == 0, "Expected the first value from Counter(2) to be 0"
assert next(c) == 1, "Expected the second value from Counter(2) to be 1"
try:
    next(c)
    raise AssertionError("expected StopIteration after stop elements")
except StopIteration:
    pass
print("generators9 ✓")