# checks/classes/classes7.py
assert g.greet() == "Hello, Alice!", f"got {g.greet()!r}"
assert Greeter("Bob").greet() == "Hello, Bob!", (
    "Greeter('Bob').greet() should return 'Hello, Bob!'; "
    "build it from self.get_name()"
)
print("classes7 ✓")
