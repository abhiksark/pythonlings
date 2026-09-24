assert Book("A", "123") == Book("B", "123"), (
    "Two books with the same ISBN should be equal"
)
assert Book("A", "123") != Book("C", "999"), (
    "Two books with different ISBNs should not be equal"
)
print("oop_advanced7 ok")
