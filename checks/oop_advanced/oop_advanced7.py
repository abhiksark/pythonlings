assert Book("A", "123") == Book("B", "123"), (
    "books with the same ISBN should compare equal"
)
assert Book("A", "123") != Book("C", "999"), (
    "books with different ISBNs should not compare equal"
)
print("oop_advanced7 ok")
