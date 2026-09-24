assert [member.name for member in Status] == ["TODO", "DOING", "DONE"], "status member names should be TODO, DOING, DONE in order"
assert [member.value for member in Status] == [1, 2, 3], "status member values should be 1,2,3 in order"
print("enums2 ok")
