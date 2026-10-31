from datetime import date

assert next_week == date(2026, 5, 30), (
    "next_week should be date(2026, 5, 30), "
    f"got {next_week!r}"
)
print("datetime2 ok")
