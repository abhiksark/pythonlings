# Tuples

Source: https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Tuples group ordered values and are commonly unpacked into multiple names.

## Extracted reference

5.3. Tuples and Sequences

We saw that lists and strings have many common properties, such as indexing and
slicing operations. They are two examples of sequence data types (see
Sequence Types — list, tuple, range). Since Python is an evolving language, other sequence data
types may be added. There is also another standard sequence data type: the
tuple.

A tuple consists of a number of values separated by commas, for instance:

```python
>>> t = 12345, 54321, 'hello!'
>>> t[0]
12345
>>> t
(12345, 54321, 'hello!')
>>> # Tuples may be nested:
>>> u = t, (1, 2, 3, 4, 5)
>>> u
((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
>>> # Tuples are immutable:
>>> t[0] = 88888
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> # but they can contain mutable objects:
>>> v = ([1, 2, 3], [3, 2, 1])
>>> v
([1, 2, 3], [3, 2, 1])

```

As you see, on output tuples are always enclosed in parentheses, so that nested
tuples are interpreted correctly; they may be input with or without surrounding
parentheses, although often parentheses are necessary anyway (if the tuple is
part of a larger expression). It is not possible to assign to the individual
items of a tuple, however it is possible to create tuples which contain mutable
objects, such as lists.

Though tuples may seem similar to lists, they are often used in different

## More reference

Source: https://docs.python.org/3/library/stdtypes.html#common-sequence-operations

Operations shared by all sequence types: indexing, slicing, concatenation.

Common Sequence Operations

The operations in the following table are supported by most sequence types,
both mutable and immutable. The `collections.abc.Sequence` ABC is
provided to make it easier to correctly implement these operations on
custom sequence types.

This table lists the sequence operations sorted in ascending priority. In the
table, s and t are sequences of the same type, n, i, j and k are
integers and x is an arbitrary object that meets any type and value
restrictions imposed by s.

The `in` and `not in` operations have the same priorities as the
comparison operations. The `+` (concatenation) and `*` (repetition)
operations have the same priority as the corresponding numeric operations. [3]

Operation

Result

Notes

`x in s`

`True` if an item of s is
equal to x, else `False`

(1)

`x not in s`

`False` if an item of s is
equal to x, else `True`

(1)

`s + t`

the concatenation of s and
t
