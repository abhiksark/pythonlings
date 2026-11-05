assert coordinates == [
    (0, "low"),
    (0, "high"),
    (1, "low"),
    (1, "high"),
], (
    "coordinates should contain every (x, y) pair from xs and ys, "
    f"got {coordinates!r}"
)
print("itertools3 ok")
