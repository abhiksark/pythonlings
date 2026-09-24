# Collections

Source: https://docs.python.org/3/library/collections.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`collections` provides specialized containers beyond the built-in list, dict, set, and tuple.

## Extracted reference

collections — Container datatypes — Python 3.14.6 documentation

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

- `collections` — Container datatypes

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/collections.html#collections.Counter

`Counter` tallies hashable objects and finds the most common ones.

class collections.Counter(**kwargs)

class collections.Counter(iterable, /, **kwargs)

class collections.Counter(mapping, /, **kwargs)

A `Counter` is a `dict` subclass for counting hashable objects.
It is a collection where elements are stored as dictionary keys
and their counts are stored as dictionary values. Counts are allowed to be
any integer value including zero or negative counts. The `Counter`
class is similar to bags or multisets in other languages.

Elements are counted from an iterable or initialized from another
mapping (or counter):

```python
>>> c = Counter() # a new, empty counter
>>> c = Counter('gallahad') # a new counter from an iterable
>>> c = Counter({'red': 4, 'blue': 2}) # a new counter from a mapping
>>> c = Counter(cats=4, dogs=8) # a new counter from keyword args

```

Counter objects have a dictionary interface except that they return a zero
count for missing items instead of raising a `KeyError`:

```python
>>> c = Counter(['eggs', 'ham'])
>>> c['bacon'] # count of a missing element is zero
0

```

Setting a count to zero does not remove an element from a counter.
Use `del` to remove it entirely:

```python
>>> c['sausage'] = 0 # counter entry with a zero count
>>> del c['sausage'] # del actually removes the entry
