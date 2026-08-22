assert repeated == ["red", "blue", "red", "blue", "red", "blue"], (
    "repeated should cycle through colors for six values, "
    f"got {repeated!r}"
)
print("itertools6 ok")
