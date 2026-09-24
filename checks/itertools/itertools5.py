assert running_totals == [3, 7, 12, 18], (
    "running_totals should contain cumulative sums [3, 7, 12, 18], "
    f"got {running_totals!r}"
)
print("itertools5 ok")
