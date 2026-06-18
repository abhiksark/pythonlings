# Sets

Source: https://docs.python.org/3/tutorial/datastructures.html#sets

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Sets store unique values and support membership tests and set operations.

## Extracted reference

5.4. Sets

Python also includes a data type for sets. A set is
an unordered collection with no duplicate elements. Basic uses include
membership testing and eliminating duplicate entries. Set objects also
support mathematical operations like union, intersection, difference, and
symmetric difference.

Curly braces or the `set()` function can be used to create sets. Note: to
create an empty set you have to use `set()`, not `{}`; the latter creates an
empty dictionary, a data structure that we discuss in the next section.

Because sets are unordered, iterating over them or printing them can
produce the elements in a different order than you expect.

Here is a brief demonstration:

```python
>>> basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
>>> print(basket) # show that duplicates have been removed
{'orange', 'banana', 'pear', 'apple'}
>>> 'orange' in basket # fast membership testing
True
>>> 'crabgrass' in basket
False

>>> # Demonstrate set operations on unique letters from two words
>>>
>>> a = set('abracadabra')
>>> b = set('alacazam')
>>> a # unique letters in a
{'a', 'r', 'b', 'c', 'd'}
>>> a - b # letters in a but not in b
{'r', 'd', 'b'}
>>> a | b # letters in a or b or both
{'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}
>>> a & b # letters in both a and b
{'a', 'c'}
>>> a ^ b # letters in a or b but not both
{'r', 'd', 'b', 'm', 'z', 'l'}

## More reference

Source: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

set and frozenset methods for membership and set relationships.

Set Types — `set`, `frozenset`

A set object is an unordered collection of distinct hashable objects.
Common uses include membership testing, removing duplicates from a sequence, and
computing mathematical operations such as intersection, union, difference, and
symmetric difference.
(For other containers see the built-in `dict`, `list`,
and `tuple` classes, and the `collections` module.)

Like other collections, sets support `x in set`, `len(set)`, and `for x in
set`. Being an unordered collection, sets do not record element position or
order of insertion. Accordingly, sets do not support indexing, slicing, or
other sequence-like behavior.

There are currently two built-in set types, `set` and `frozenset`.
The `set` type is mutable — the contents can be changed using methods
like `add()` and `remove()`.
Since it is mutable, it has no hash value and cannot be used as
either a dictionary key or as an element of another set.
The `frozenset` type is immutable and hashable —
its contents cannot be altered after it is created;
it can therefore be used as a dictionary key or as an element of another set.

Non-empty sets (not frozensets) can be created by placing a comma-separated list
of elements within braces, for example: `{'jack', 'sjoerd'}`, in addition to the
`set` constructor.

The constructors for both classes work the same:

class set(iterable=(), /)

class frozenset(iterable=(), /)

Return a new set or frozenset object whose elements are taken from
iterable. The elements of a set must be hashable. To
represent sets of sets, the inner sets must be `frozenset`
objects. If iterable is not specified, a new empty set is
returned.

Sets can be created by several means:
