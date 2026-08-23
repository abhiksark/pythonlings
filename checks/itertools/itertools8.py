assert flattened == [1, 2, 3, 4, 5], (
    "flattened should contain all batch items in order, "
    f"got {flattened!r}"
)
assert adjacent_pairs == [(1, 2), (2, 3), (3, 4), (4, 5)], (
    "adjacent_pairs should contain each neighboring pair, "
    f"got {adjacent_pairs!r}"
)
print("itertools8 ok")
