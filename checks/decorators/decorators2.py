assert loud_greet() == "HELLO", (
    f"loud_greet() should return 'HELLO', got {loud_greet()!r}"
)
assert shout(lambda: "world")() == "WORLD", (
    f"shout(lambda: 'world')() should return 'WORLD', got {shout(lambda: 'world')()!r}"
)
print("decorators2 ✓")
