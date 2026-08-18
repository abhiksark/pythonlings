assert slow_square(4) == 16, f"slow_square(4) should return 16, got {slow_square(4)}"
assert slow_square(5) == 25, f"slow_square(5) should return 25, got {slow_square(5)}"
# Second calls must hit the cache, not recompute
assert (
    slow_square(4) == 16
), f"cached slow_square(4) call should return 16, got {slow_square(4)}"
assert (
    slow_square(5) == 25
), f"cached slow_square(5) call should return 25, got {slow_square(5)}"
assert call_count == 2, (
    f"slow_square should have been called exactly 2 times (once per unique arg), "
    f"but call_count is {call_count}"
)
assert (4,) in slow_square.cache, "cache should contain key (4,) for arg 4"
assert (
    slow_square.cache[(4,)] == 16
), f"slow_square.cache[(4,)] should be 16, got {slow_square.cache[(4,)]}"
print("decorators10 ✓")
