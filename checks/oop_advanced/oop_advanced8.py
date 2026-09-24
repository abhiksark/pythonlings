coord = Coordinate.from_text("3,4")
assert (coord.x, coord.y) == (3, 4), (
    f"Coordinate.from_text('3,4') should produce (3, 4), "
    f"got {(coord.x, coord.y)!r}"
)
print("oop_advanced8 ok")
