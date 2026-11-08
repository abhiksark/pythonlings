assert add(3, 4) == 7, f"add(3, 4) should return 7, got {add(3, 4)!r}"
assert add(10, -2) == 8, f"add(10, -2) should return 8, got {add(10, -2)!r}"
assert greet("Alice") == "Hello, Alice!", (
    f"greet('Alice') should return 'Hello, Alice!', got {greet('Alice')!r}"
)
assert greet("Bob", greeting="Hi") == "Hi, Bob!", (
    f"greet('Bob', greeting='Hi') should return 'Hi, Bob!', got {greet('Bob', greeting='Hi')!r}"
)
print("decorators5 ✓")
