assert origin.x == 0 and origin.y == 0, (
    f"expected origin at (0, 0), got ({origin.x}, {origin.y})"
)
assert Point(2, 5).x == 2 and Point(2, 5).y == 5, (
    f"expected Point(2, 5) to have x=2 and y=5, "
    f"got x={Point(2, 5).x} and y={Point(2, 5).y}"
)
print("dataclasses1 ✓")
