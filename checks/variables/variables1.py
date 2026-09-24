# checks/variables/variables1.py
assert isinstance(a, int), "a should be an integer"
assert isinstance(b, float), "b should be a float"
assert isinstance(c, str), "c should be a string"
assert a == 0, "a should be 0 — the default value from the exercise"
assert b == 0.0, "b should be 0.0 — a float, not an int"
assert c == "", "c should be an empty string"
print("variables1 ✓")
