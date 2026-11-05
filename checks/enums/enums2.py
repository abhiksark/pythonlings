assert [member.name for member in Status] == ["TODO", "DOING", "DONE"], (
    "Status names should be ['TODO', 'DOING', 'DONE'], got "
    f"{[member.name for member in Status]!r}"
)
assert [member.value for member in Status] == [1, 2, 3], (
    f"Status values should be [1, 2, 3], got "
    f"{[member.value for member in Status]!r}"
)
print("enums2 ok")
