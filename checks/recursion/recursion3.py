# checks/recursion/recursion3.py
assert recursive_sum([]) == 0, "recursive_sum([]) should be 0"
assert recursive_sum([5]) == 5, "recursive_sum([5]) should be 5"
assert recursive_sum([1, 2, 3]) == 6, "recursive_sum([1, 2, 3]) should be 6"
assert recursive_sum([10, 20, 30, 40]) == 100, (
    "recursive_sum([10, 20, 30, 40]) should be 100"
)
assert recursive_sum([-1, -2, 3]) == 0, "recursive_sum([-1, -2, 3]) should be 0"
print("recursion3 ✓")
