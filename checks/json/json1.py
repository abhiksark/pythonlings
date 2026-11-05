# checks/json/json1.py
assert data == {"name": "Ada", "language": "Python"}, (
    "data should be {'name': 'Ada', 'language': 'Python'}, "
    f"got {data!r}"
)
assert name == "Ada", f"name should be 'Ada', got {name!r}"
print("json1 ok")
