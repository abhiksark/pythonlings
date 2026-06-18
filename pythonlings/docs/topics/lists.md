# Lists

Source: https://docs.python.org/3/tutorial/datastructures.html#more-on-lists

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Lists are mutable ordered collections with methods such as `append`, `pop`, and `sort`.

## Extracted reference

5.1. More on Lists

The list data type has some more methods. Here are all
of the methods of list objects:

list.append(value, /)

Add an item to the end of the list. Similar to `a[len(a):] = [x]`.

list.extend(iterable, /)

Extend the list by appending all the items from the iterable. Similar to
`a[len(a):] = iterable`.

list.insert(index, value, /)

Insert an item at a given position. The first argument is the index of the
element before which to insert, so `a.insert(0, x)` inserts at the front of
the list, and `a.insert(len(a), x)` is equivalent to `a.append(x)`.

list.remove(value, /)

Remove the first item from the list whose value is equal to value. It raises a
`ValueError` if there is no such item.

list.pop(index=-1, /)

Remove the item at the given position in the list, and return it. If no index
is specified, `a.pop()` removes and returns the last item in the list.
It raises an `IndexError` if the list is empty or the index is
outside the list range.

list.clear()

Remove all items from the list. Similar to `del a[:]`.

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list.
Raises a `ValueError` if there is no such item.

## More reference

Source: https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range

Sequence types reference with list methods, operations, and type tables.

Sequence Types — `list`, `tuple`, `range`

There are three basic sequence types: lists, tuples, and range objects.
Additional sequence types tailored for processing of
binary data and text strings are
described in dedicated sections.

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
