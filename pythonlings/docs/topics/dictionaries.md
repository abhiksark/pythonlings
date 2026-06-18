# Dictionaries

Source: https://docs.python.org/3/tutorial/datastructures.html#dictionaries

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Dictionaries map keys to values and are the standard way to represent lookup tables.

## Extracted reference

5.5. Dictionaries

Another useful data type built into Python is the dictionary (see
Mapping Types — dict). Dictionaries are sometimes found in other languages as
“associative memories” or “associative arrays”. Unlike sequences, which are
indexed by a range of numbers, dictionaries are indexed by keys, which can be
any immutable type; strings and numbers can always be keys. Tuples can be used
as keys if they contain only strings, numbers, or tuples; if a tuple contains
any mutable object either directly or indirectly, it cannot be used as a key.
You can’t use lists as keys, since lists can be modified in place using index
assignments, slice assignments, or methods like `append()` and
`extend()`.

It is best to think of a dictionary as a set of key: value pairs,
with the requirement that the keys are unique (within one dictionary). A pair of
braces creates an empty dictionary: `{}`. Placing a comma-separated list of
key:value pairs within the braces adds initial key:value pairs to the
dictionary; this is also the way dictionaries are written on output.

The main operations on a dictionary are storing a value with some key and
extracting the value given the key. It is also possible to delete a key:value
pair with `del`. If you store using a key that is already in use, the old
value associated with that key is forgotten.

Extracting a value for a non-existent key by subscripting (`d[key]`) raises a
`KeyError`. To avoid getting this error when trying to access a possibly
non-existent key, use the `get()` method instead, which returns
`None` (or a specified default value) if the key is not in the dictionary.

Performing `list(d)` on a dictionary returns a list of all the keys
used in the dictionary, in insertion order (if you want it sorted, just use
`sorted(d)` instead). To check whether a single key is in the
dictionary, use the `in` keyword.

Here is a small example using a dictionary:

```python
>>> tel = {'jack': 4098, 'sape': 4139}
>>> tel['guido'] = 4127
>>> tel

## More reference

Source: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

The dict type with constructor forms, methods, and creation examples.

Mapping Types — `dict`

A mapping object maps hashable values to arbitrary objects.
Mappings are mutable objects. There is currently only one standard mapping
type, the dictionary. (For other containers see the built-in
`list`, `set`, and `tuple` classes, and the
`collections` module.)

A dictionary’s keys are almost arbitrary values. Values that are not
hashable, that is, values containing lists, dictionaries or other
mutable types (that are compared by value rather than by object identity) may
not be used as keys.
Values that compare equal (such as `1`, `1.0`, and `True`)
can be used interchangeably to index the same dictionary entry.

class dict(**kwargs)

class dict(mapping, /, **kwargs)

class dict(iterable, /, **kwargs)

Return a new dictionary initialized from an optional positional argument
and a possibly empty set of keyword arguments.

Dictionaries can be created by several means:

-

Use a comma-separated list of `key: value` pairs within braces:
`{'jack': 4098, 'sjoerd': 4127}` or `{4098: 'jack', 4127: 'sjoerd'}`

-

Use a dict comprehension: `{}`, `{x: x ** 2 for x in range(10)}`

-

Use the type constructor: `dict()`,
`dict([('foo', 100), ('bar', 200)])`, `dict(foo=100, bar=200)`
