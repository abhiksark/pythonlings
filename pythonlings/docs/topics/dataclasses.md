# Dataclasses

Source: https://docs.python.org/3/library/dataclasses.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Dataclasses generate common class methods for data-focused classes.

## Extracted reference

dataclasses — Data Classes — Python 3.14.6 documentation

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

- Python Runtime Services »

- `dataclasses` — Data Classes

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables

Class vs instance variables — the distinction behind dataclass fields.

9.3.5. Class and Instance Variables

Generally speaking, instance variables are for data unique to each instance
and class variables are for attributes and methods shared by all instances
of the class:

```python
class Dog:

kind = 'canine' # class variable shared by all instances

def __init__(self, name):
self.name = name # instance variable unique to each instance

>>> d = Dog('Fido')
>>> e = Dog('Buddy')
>>> d.kind # shared by all dogs
'canine'
>>> e.kind # shared by all dogs
'canine'
>>> d.name # unique to d
'Fido'
>>> e.name # unique to e
'Buddy'

```

As discussed in A Word About Names and Objects, shared data can have possibly surprising
effects involving mutable objects such as lists and dictionaries.
For example, the tricks list in the following code should not be used as a
class variable because just a single list would be shared by all Dog
instances:

```python
class Dog:

tricks = [] # mistaken use of a class variable

def __init__(self, name):
self.name = name
