# checks/functional/functional8.py
assert product == 120, f"product should be 120, got {product}"

from functools import reduce

assert reduce(lambda a, b: a * b, [2, 3, 4]) == 24, (
    "product of [2, 3, 4] should be 24"
)
assert reduce(lambda a, b: a + b, [1, 2, 3, 4]) == 10, (
    "sum of [1, 2, 3, 4] should be 10"
)
print("functional8 ✓")
