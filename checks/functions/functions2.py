# checks/functions/functions2.py
assert callable(greet), "greet should be a function"
assert greet() == "hello", "greet() should return 'hello'"
assert message == "hello", f"message should be 'hello', got {message!r}"
print("functions2 ✓")
