# checks/oop_advanced/oop_advanced2.py
employee = Employee("Ada", "Engineer")
assert employee.name == "Ada", f"expected name 'Ada', got {employee.name!r}"
assert employee.role == "Engineer", (
    f"expected role 'Engineer', got {employee.role!r}"
)
print("oop_advanced2 ok")
