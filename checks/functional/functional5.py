# checks/functional/functional5.py
assert by_length == ["fig", "kiwi", "date", "apple", "banana"], (
    "by_length should be ['fig', 'kiwi', 'date', 'apple', 'banana'], "
    f"got {by_length}"
)
assert by_length[0] == "fig", (
    f"by_length[0] should be 'fig', got {by_length[0]}"
)
assert by_length[-1] == "banana", (
    f"by_length[-1] should be 'banana', got {by_length[-1]}"
)
print("functional5 ✓")
