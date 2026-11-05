# checks/json/json2.py
assert text == '{"a": 1, "b": 2}', (
    'text should be \'{"a": 1, "b": 2}\', '
    f"got {text!r}"
)
print("json2 ok")
