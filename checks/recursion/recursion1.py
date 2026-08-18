assert countdown(0) == [0], f"countdown(0) should return [0], got {countdown(0)!r}"
assert countdown(1) == [1, 0], f"countdown(1) should return [1, 0], got {countdown(1)!r}"
assert countdown(3) == [3, 2, 1, 0], f"countdown(3) should return [3, 2, 1, 0], got {countdown(3)!r}"
assert countdown(5) == [5, 4, 3, 2, 1, 0], f"countdown(5) should return [5, 4, 3, 2, 1, 0], got {countdown(5)!r}"
print("recursion1 ✓")
