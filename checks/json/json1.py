assert data == {"name": "Ada", "language": "Python"}, (
    f"data should contain Ada and Python, got {data!r}"
)
assert name == "Ada", f"name should be 'Ada', got {name!r}"
print("json1 ok")
