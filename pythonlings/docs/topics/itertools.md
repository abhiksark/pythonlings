# Itertools

Source: https://docs.python.org/3/library/itertools.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`itertools` provides fast iterator building blocks for loops and data pipelines.

## Extracted reference

itertools — Functions creating iterators for efficient looping — Python 3.14.6 documentation

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

- Functional Programming Modules »

- `itertools` — Functions creating iterators for efficient looping

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/howto/functional.html#the-itertools-module

The functional HOWTO's tour of itertools with examples.

The itertools module

The `itertools` module contains a number of commonly used iterators as well
as functions for combining several iterators. This section will introduce the
module’s contents by showing small examples.

The module’s functions fall into a few broad classes:

-

Functions that create a new iterator based on an existing iterator.

-

Functions for treating an iterator’s elements as function arguments.

-

Functions for selecting portions of an iterator’s output.

-

A function for grouping an iterator’s output.

Creating new iterators

`itertools.count(start, step)` returns an infinite
stream of evenly spaced values. You can optionally supply the starting number,
which defaults to 0, and the interval between numbers, which defaults to 1:

```python
itertools.count() =>
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...
itertools.count(10) =>
10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...
itertools.count(10, 5) =>
10, 15, 20, 25, 30, 35, 40, 45, 50, 55, ...

```
