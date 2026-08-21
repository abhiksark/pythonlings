# checks/datetime/datetime8.py
from datetime import date

assert earliest == date(2024, 1, 1), f"Expected earliest date to be date(2024, 1, 1), got {earliest!r}"
assert latest == date(2026, 5, 23), f"Expected latest date to be date(2026, 5, 23), got {latest!r}"
print("datetime8 ok")
