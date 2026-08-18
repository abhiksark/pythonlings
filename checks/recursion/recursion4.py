assert count_items([]) == 0, f"count_items([]) should return 0, got {count_items([])!r}"
assert count_items([42]) == 1, f"count_items([42]) should return 1, got {count_items([42])!r}"
assert count_items([1, 2, 3]) == 3, f"count_items([1, 2, 3]) should return 3, got {count_items([1, 2, 3])!r}"
assert count_items(["a", "b", "c", "d"]) == 4, f'count_items(["a", "b", "c", "d"]) should return 4, got {count_items(["a", "b", "c", "d"])!r}'
assert count_items(list(range(10))) == 10, f"count_items(list(range(10))) should return 10, got {count_items(list(range(10)))!r}"
print("recursion4 ✓")
