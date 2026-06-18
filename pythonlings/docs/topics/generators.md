# Generators

Source: https://docs.python.org/3/tutorial/classes.html#generators

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Generators produce values lazily with `yield` instead of returning a whole collection.

## Extracted reference

9.9. Generators

Generators are a simple and powerful tool for creating iterators. They
are written like regular functions but use the `yield` statement
whenever they want to return data. Each time `next()` is called on it, the
generator resumes where it left off (it remembers all the data values and which
statement was last executed). An example shows that generators can be trivially
easy to create:

```python
def reverse(data):
for index in range(len(data)-1, -1, -1):
yield data[index]

```

```python
>>> for char in reverse('golf'):
... print(char)
...
f
l
o
g

```

Anything that can be done with generators can also be done with class-based
iterators as described in the previous section. What makes generators so
compact is that the `__iter__()` and `__next__()` methods
are created automatically.

Another key feature is that the local variables and execution state are
automatically saved between calls. This made the function easier to write and
much more clear than an approach using instance variables like `self.index`
and `self.data`.

In addition to automatic method creation and saving program state, when
generators terminate, they automatically raise `StopIteration`. In
combination, these features make it easy to create iterators with no more effort

## More reference

Source: https://docs.python.org/3/reference/expressions.html#generator-expressions

Generator expression syntax for compact lazy iterators.

6.2.9. Generator expressions

The syntax for generator expressions is the same as for
list comprehensions, except that they are enclosed in
parentheses instead of brackets.
For example:

```python
>>> iterator = (x ** 2 for x in range(10))
>>> iterator
<generator object <genexpr> at ...>

```

At runtime, a generator expression evaluates to a generator iterator
which yields the same values as the corresponding list comprehension:

```python
>>> list(iterator)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

```

Thus, the example above is roughly equivalent to defining and calling
the following generator function:

```python
def make_generator_of_squares(iterator):
for x in iterator:
yield x ** 2

make_generator_of_squares(iter(range(10)))

```

The enclosing parentheses can be omitted in calls when the generator
expression is the only positional argument and there are no keyword
arguments.
See the Calls section for details.
For example:
