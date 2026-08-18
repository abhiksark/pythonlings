assert callable(greet), "greet should be a function"
assert greet() == "hello", f"greet() should return 'hello', got {greet()!r}"
assert message == "hello", f"message should be 'hello', got {message!r}"
print("functions2 ✓")
