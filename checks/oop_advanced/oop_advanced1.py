# checks/oop_advanced/oop_advanced1.py
dog = Dog()
assert isinstance(dog, Animal), "Dog() should be an instance of Animal"
assert dog.speak() == "sound", "Dog().speak() should return 'sound'"
print("oop_advanced1 ok")
