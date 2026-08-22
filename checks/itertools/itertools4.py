assert grouped == {
    "fruit": ["apple", "pear"],
    "veg": ["carrot"],
}, (
    "grouped should map each category to its item names, "
    f"got {grouped!r}"
)
print("itertools4 ok")
