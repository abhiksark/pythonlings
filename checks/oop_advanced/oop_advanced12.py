result = Vector(1, 2) + Vector(3, 4)
assert isinstance(result, Vector), (
    f"Adding two Vector instances should return a Vector, "
    f"got {type(result).__name__}"
)
assert (result.x, result.y) == (4, 6), (
    f"Vector(1, 2) + Vector(3, 4) should be (4, 6), "
    f"got {(result.x, result.y)!r}"
)
print("oop_advanced12 ok")
