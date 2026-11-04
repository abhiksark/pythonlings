# checks/functional/functional9.py
assert has_negative is True, f"has_negative should be True, got {has_negative}"
assert all_positive is True, f"all_positive should be True, got {all_positive}"

assert any(x < 0 for x in [1, 2, -3]) is True, (
    "any(x < 0 for x in [1, 2, -3]) should be True: -3 is negative"
)
assert any(x < 0 for x in [1, 2, 3]) is False, (
    "any(x < 0 for x in [1, 2, 3]) should be False: all are positive"
)
assert all(x > 0 for x in [1, 2, 3]) is True, (
    "all(x > 0 for x in [1, 2, 3]) should be True: all are positive"
)
assert all(x > 0 for x in [1, -2, 3]) is False, (
    "all(x > 0 for x in [1, -2, 3]) should be False: -2 is not > 0"
)
print("functional9 ✓")
