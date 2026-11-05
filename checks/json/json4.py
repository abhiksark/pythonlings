# checks/json/json4.py
assert restored == {"ok": True, "count": 3}, (
    f"restored should be {{'ok': True, 'count': 3}}, got {restored!r}"
)
print("json4 ok")
