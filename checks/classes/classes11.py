# checks/classes/classes11.py
assert isinstance(
    t, Temperature
), "from_string should return a Temperature instance"
assert t.degrees == 36.6, f"expected 36.6, got {t.degrees}"
assert boiling.degrees == 100.0, (
    f"from_string('100C') should give degrees 100.0, " f"got {boiling.degrees}"
)
assert isinstance(
    Temperature.from_string("0C"), Temperature
), "from_string('0C') should return a Temperature instance"
print("classes11 ✓")
