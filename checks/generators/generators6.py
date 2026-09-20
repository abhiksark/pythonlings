# generators6.py — first assert unchanged; big/1000 are plain variables, safe to echo
assert first_ten == list(range(1, 11)), (
    f"expected [1..10], got {first_ten}"
)
big = list(itertools.islice(natural_numbers(), 1000))
assert len(big) == 1000, f"Expected 1000 values pulled from natural_numbers(), got {len(big)}"
assert big[-1] == 1000, f"Expected the 1000th value to be 1000, got {big[-1]!r}"
print("generators6 ✓")