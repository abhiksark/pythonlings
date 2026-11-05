# checks/classes/classes8.py
assert str(book) == "Book: 1984 by Orwell", f"got {str(book)!r}"
assert (
    str(Book("Dune", "Herbert")) == "Book: Dune by Herbert"
), "str(Book('Dune', 'Herbert')) should be 'Book: Dune by Herbert'"
print("classes8 ✓")
