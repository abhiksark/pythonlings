# Functional Tools

Source: https://docs.python.org/3/howto/functional.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Functional style uses functions, iterators, and transformations as building blocks.

## Extracted reference

Functional Programming HOWTO — Python 3.14.6 documentation

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

- Python HOWTOs »

- Functional Programming HOWTO

-

|

-

Theme

Auto

## More reference

Source: https://docs.python.org/3/library/itertools.html#itertool-functions

itertools building blocks with signatures and usage patterns.

Itertool Functions

The following functions all construct and return iterators. Some provide
streams of infinite length, so they should only be accessed by functions or
loops that truncate the stream.

itertools.accumulate(iterable[, function, *, initial=None])

Make an iterator that returns accumulated sums or accumulated
results from other binary functions.

The function defaults to addition. The function should accept
two arguments, an accumulated total and a value from the iterable.

If an initial value is provided, the accumulation will start with
that value and the output will have one more element than the input
iterable.

Roughly equivalent to:

```python
def accumulate(iterable, function=operator.add, *, initial=None):
'Return running totals'
# accumulate([1,2,3,4,5]) → 1 3 6 10 15
# accumulate([1,2,3,4,5], initial=100) → 100 101 103 106 110 115
# accumulate([1,2,3,4,5], operator.mul) → 1 2 6 24 120

iterator = iter(iterable)
total = initial
if initial is None:
try:
total = next(iterator)
except StopIteration:
return

yield total
for element in iterator:
total = function(total, element)
yield total
