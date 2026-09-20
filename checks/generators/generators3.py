# generators3.py — first assert already has a message, leave it exactly as-is
assert collected == [2, 4, 6, 8], f"expected [2, 4, 6, 8], got {collected}"
assert list(evens_up_to(5)) == [2, 4], "Expected list(evens_up_to(5)) to be [2, 4]"
assert list(evens_up_to(1)) == [], "Expected list(evens_up_to(1)) to be [] (no even numbers \u2264 1)"
print("generators3 ✓")