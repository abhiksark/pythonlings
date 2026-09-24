# Enums

Source: https://docs.python.org/3/library/enum.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Enums define named constant values that are easier to read than raw literals.

## Extracted reference

enum — Support for enumerations — Python 3.14.6 documentation

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

- The Python Standard Library »

- Data Types »

- `enum` — Support for enumerations

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/enum.html#enum.Flag

`Flag` enums combine members with bitwise operators.

class enum.Flag

`Flag` is the same as `Enum`, but its members support the bitwise
operators `&` (AND), `|` (OR), `^` (XOR), and `~` (INVERT);
the results of those operations are (aliases of) members of the enumeration.

__contains__(self, value)

Returns True if value is in self:

```python
>>> from enum import Flag, auto
>>> class Color(Flag):
... RED = auto()
... GREEN = auto()
... BLUE = auto()
...
>>> purple = Color.RED | Color.BLUE
>>> white = Color.RED | Color.GREEN | Color.BLUE
>>> Color.GREEN in purple
False
>>> Color.GREEN in white
True
>>> purple in white
True
>>> white in purple
False

```

__iter__(self)

Returns all contained non-alias members:

```python
>>> list(Color.RED)
[<Color.RED: 1>]
>>> list(purple)
[<Color.RED: 1>, <Color.BLUE: 4>]
