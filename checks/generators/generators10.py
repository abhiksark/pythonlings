# generators10.py
assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10], "Expected list(running_total([1, 2, 3, 4])) to be [1, 3, 6, 10]"
assert list(running_total([10, -3, 7])) == [10, 7, 14], "Expected list(running_total([10, -3, 7])) to be [10, 7, 14]"
assert list(running_total([])) == [], "Expected list(running_total([])) to be [] (no elements to sum)"
assert list(running_total([5])) == [5], "Expected list(running_total([5])) to be [5]"
assert list(running_total(x * x for x in range(1, 5))) == [1, 5, 14, 30], "Expected running_total over a generator input (1, 4, 9, 16) to yield [1, 5, 14, 30]"
print("generators10 ✓")