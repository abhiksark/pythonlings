# checks/datetime/datetime3.py
assert meeting.year == 2026, (
    f"meeting.year should be 2026, got {meeting.year!r}"
)
assert meeting.month == 5, (
    f"meeting.month should be 5, got {meeting.month!r}"
)
assert meeting.day == 23, (
    f"meeting.day should be 23, got {meeting.day!r}"
)
assert meeting.hour == 9, (
    f"meeting.hour should be 9, got {meeting.hour!r}"
)
assert meeting.minute == 30, (
    f"meeting.minute should be 30, got {meeting.minute!r}"
)
print("datetime3 ok")
