# generators7.py — first assert unchanged
import itertools

first8 = list(itertools.islice(fibonacci(), 8))
assert first8 == [0, 1, 1, 2, 3, 5, 8, 13], (
    f"expected [0, 1, 1, 2, 3, 5, 8, 13], got {first8}"
)
first15 = list(itertools.islice(fibonacci(), 15))
assert len(first15) == 15, f"Expected 15 terms from fibonacci(), got {len(first15)}"
assert first15[-1] == 377, f"Expected the 15th Fibonacci term to be 377, got {first15[-1]!r}"
print("generators7 ✓")