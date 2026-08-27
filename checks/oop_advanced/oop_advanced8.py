coord = Coordinate.from_text("3,4")
assert (coord.x, coord.y) == (3, 4), (
    f"coord should be (3, 4), got {(coord.x, coord.y)!r}"
)
print("oop_advanced8 ok")
