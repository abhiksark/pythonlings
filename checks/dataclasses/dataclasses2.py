assert orange.red == 255, f"expected red=255, got {orange.red}"
assert orange.green == 128, f"expected green=128, got {orange.green}"
assert orange.blue == 0, f"expected blue=0, got {orange.blue}"
assert description == "R=255 G=128 B=0", f"got {description!r}"
print("dataclasses2 ✓")
