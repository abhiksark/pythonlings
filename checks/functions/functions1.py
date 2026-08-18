assert average(2, 4) == 3, f"average(2, 4) should return 3, got {average(2, 4)!r}"
assert average(10, 20) == 15, f"average(10, 20) should return 15, got {average(10, 20)!r}"
assert average(-2, -4) == -3, f"average(-2, -4) should return -3, got {average(-2, -4)!r}"
assert average(-10, -20) == -15, f"average(-10, -20) should return -15, got {average(-10, -20)!r}"
assert average(1.5, 2.5) == 2, f"average(1.5, 2.5) should return 2, got {average(1.5, 2.5)!r}"
assert average(0.5, 1.5) == 1, f"average(0.5, 1.5) should return 1, got {average(0.5, 1.5)!r}"
assert average(0, 0) == 0, f"average(0, 0) should return 0, got {average(0, 0)!r}"
assert average(3, 4.5) == 3.75, f"average(3, 4.5) should return 3.75, got {average(3, 4.5)!r}"
print("functions1 ✓")
