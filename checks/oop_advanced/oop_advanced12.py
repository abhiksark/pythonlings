result = Vector(1, 2) + Vector(3, 4)
assert isinstance(result, Vector), "result should be a Vector"
assert (result.x, result.y) == (4, 6), (
    f"result coordinates should be (4, 6), got {(result.x, result.y)!r}"
)
print("oop_advanced12 ok")
