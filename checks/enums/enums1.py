assert Color.RED.value == "red", (
    f"Color.RED.value should be 'red', got {Color.RED.value!r}"
)
assert Color.BLUE.value == "blue", (
    f"Color.BLUE.value should be 'blue', got {Color.BLUE.value!r}"
)
assert favorite is Color.RED, (
    f"favorite should be Color.RED, got {favorite!r}"
)
print("enums1 ok")
