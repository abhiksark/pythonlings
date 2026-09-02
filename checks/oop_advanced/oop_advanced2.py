employee = Employee("Ada", "Engineer")
assert employee.name == "Ada", (
    f"employee.name should be 'Ada', got {employee.name!r}"
)
assert employee.role == "Engineer", (
    f"employee.role should be 'Engineer', got {employee.role!r}"
)
print("oop_advanced2 ok")
