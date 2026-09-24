assert pairs == [("a", 1), ("b", "?"), ("c", "?")], (
    "pairs should fill missing right-side values with '?', "
    f"got {pairs!r}"
)
print("itertools7 ok")
