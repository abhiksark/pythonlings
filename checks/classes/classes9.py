# checks/classes/classes9.py
assert repr(c) == "Color(r=255, g=128, b=0)", f"got {repr(c)!r}"
assert str(c) == "rgb(255, 128, 0)", (
    "str(c) should stay 'rgb(255, 128, 0)'; add __repr__ without "
    "changing __str__"
)
assert repr(Color(0, 0, 0)) == "Color(r=0, g=0, b=0)", (
    "repr(Color(0, 0, 0)) should be 'Color(r=0, g=0, b=0)'; "
    "use the instance values"
)
print("classes9 ✓")
