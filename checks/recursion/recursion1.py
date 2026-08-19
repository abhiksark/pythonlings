# checks/recursion/recursion1.py
assert countdown(0) == [0], "countdown(0) should return [0]"
assert countdown(1) == [1, 0], "countdown(1) should return [1, 0]"
assert countdown(3) == [3, 2, 1, 0], "countdown(3) should return [3, 2, 1, 0]"
assert countdown(5) == [5, 4, 3, 2, 1, 0], (
    "countdown(5) should return [5, 4, 3, 2, 1, 0]"
)
print("recursion1 ✓")
