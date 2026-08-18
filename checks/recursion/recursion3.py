assert recursive_sum([]) == 0, f"recursive_sum([]) should be 0, got {recursive_sum([])!r}"
assert recursive_sum([5]) == 5, f"recursive_sum([5]) should be 5, got {recursive_sum([5])!r}"
assert recursive_sum([1, 2, 3]) == 6, f"recursive_sum([1, 2, 3]) should be 6, got {recursive_sum([1, 2, 3])!r}"
assert recursive_sum([10, 20, 30, 40]) == 100, f"recursive_sum([10, 20, 30, 40]) should be 100, got {recursive_sum([10, 20, 30, 40])!r}"
assert recursive_sum([-1, -2, 3]) == 0, f"recursive_sum([-1, -2, 3]) should be 0, got {recursive_sum([-1, -2, 3])!r}"
print("recursion3 ✓")
