# generators1.py
assert list(count_up_to(4)) == [1, 2, 3, 4], "Expected list(count_up_to(4)) to be [1, 2, 3, 4]"
assert list(count_up_to(1)) == [1], "Expected list(count_up_to(1)) to be [1]"
assert list(count_up_to(0)) == [], "Expected list(count_up_to(0)) to be [] (no elements when limit is 0)"
print("generators1 ✓")