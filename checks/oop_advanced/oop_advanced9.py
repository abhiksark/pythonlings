assert Grade.is_valid(0) is True, "Grade 0 should be a valid score"
assert Grade.is_valid(100) is True, "Grade 100 should be a valid score"
assert Grade.is_valid(101) is False, (
    "Grade 101 should be rejected as out of range"
)
print("oop_advanced9 ok")
