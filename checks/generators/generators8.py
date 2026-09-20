# generators8.py — Countdown is the class under test, no re-invocation in messages
assert list(Countdown(3)) == [3, 2, 1], "Expected list(Countdown(3)) to be [3, 2, 1]"
assert list(Countdown(1)) == [1], "Expected list(Countdown(1)) to be [1]"
assert list(Countdown(5)) == [5, 4, 3, 2, 1], "Expected list(Countdown(5)) to be [5, 4, 3, 2, 1]"
cd = Countdown(3)
assert list(cd) == [3, 2, 1], "Expected first iteration over cd to be [3, 2, 1]"
assert list(cd) == [3, 2, 1], "Expected second iteration over cd to also be [3, 2, 1] \u2014 Countdown should be re-iterable, not exhausted after one pass"
print("generators8 ✓")