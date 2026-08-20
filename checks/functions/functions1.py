# checks/functions/functions1.py
assert average(2, 4) == 3, "average(2, 4) should return 3"
assert average(10, 20) == 15, "average(10, 20) should return 15"
assert average(-2, -4) == -3, "average(-2, -4) should return -3"
assert average(-10, -20) == -15, "average(-10, -20) should return -15"
assert average(1.5, 2.5) == 2, "average(1.5, 2.5) should return 2"
assert average(0.5, 1.5) == 1, "average(0.5, 1.5) should return 1"
assert average(0, 0) == 0, "average(0, 0) should return 0"
assert average(3, 4.5) == 3.75, "average(3, 4.5) should return 3.75"
print("functions1 ✓")
