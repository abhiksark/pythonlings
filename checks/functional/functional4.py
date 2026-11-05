# checks/functional/functional4.py
assert evens == [2, 4, 6, 8, 10], (
    f"evens should be [2, 4, 6, 8, 10], got {evens}"
)
assert isinstance(evens, list), (
    f"evens should be a list, got {type(evens).__name__}"
)
assert all(x % 2 == 0 for x in evens), (
    f"evens should contain only even numbers, got {evens}"
)
print("functional4 ✓")
