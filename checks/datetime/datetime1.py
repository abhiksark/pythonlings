# checks/datetime/datetime1.py
from datetime import date

assert launch_day == date(2026, 5, 23), (
    "launch_day should be date(2026, 5, 23), "
    f"got {launch_day!r}"
)
print("datetime1 ok")
