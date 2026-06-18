# Advanced OOP

Source: https://docs.python.org/3/tutorial/classes.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Advanced class patterns build on attributes, methods, inheritance, and special methods.

## Extracted reference

9. Classes — Python 3.14.6 documentation

Navigation

-
index

-
modules |

-
next |

-
previous |

-

- Python »

-

-

-
3.14.6 Documentation »

- The Python Tutorial »

- 9. Classes

-

|

-

Theme

Auto

## More reference

Source: https://docs.python.org/3/reference/datamodel.html#object.__repr__

`__repr__` and `__str__` for custom object representations.

object.__repr__(self)

Called by the `repr()` built-in function to compute the “official” string
representation of an object. If at all possible, this should look like a
valid Python expression that could be used to recreate an object with the
same value (given an appropriate environment). If this is not possible, a
string of the form `<...some useful description...>` should be returned.
The return value must be a string object. If a class defines `__repr__()`
but not `__str__()`, then `__repr__()` is also used when an
“informal” string representation of instances of that class is required.

This is typically used for debugging, so it is important that the representation
is information-rich and unambiguous. A default implementation is provided by the
`object` class itself.
