# checks/recursion/recursion4.py
assert count_items([]) == 0, "count_items([]) should return 0"
assert count_items([42]) == 1, "count_items([42]) should return 1"
assert count_items([1, 2, 3]) == 3, "count_items([1, 2, 3]) should return 3"
assert count_items(["a", "b", "c", "d"]) == 4, (
    'count_items(["a", "b", "c", "d"]) should return 4'
)
assert count_items(list(range(10))) == 10, (
    "count_items(list(range(10))) should return 10"
)
print("recursion4 ✓")
