# Comprehensions

Source: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Comprehensions build new collections by combining an expression with one or more loops.

## Extracted reference

5.1.3. List Comprehensions

List comprehensions provide a concise way to create lists.
Common applications are to make new lists where each element is the result of
some operations applied to each member of another sequence or iterable, or to
create a subsequence of those elements that satisfy a certain condition.

For example, assume we want to create a list of squares, like:

```python
>>> squares = []
>>> for x in range(10):
... squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

```

Note that this creates (or overwrites) a variable named `x` that still exists
after the loop completes. We can calculate the list of squares without any
side effects using:

```python
squares = list(map(lambda x: x**2, range(10)))

```

or, equivalently:

```python
squares = [x**2 for x in range(10)]

```

which is more concise and readable.

A list comprehension consists of brackets containing an expression followed
by a `for` clause, then zero or more `for` or `if`
clauses. The result will be a new list resulting from evaluating the expression

## More reference

Source: https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions

Nested comprehensions that build lists of lists from multiple loops.

5.1.4. Nested List Comprehensions

The initial expression in a list comprehension can be any arbitrary expression,
including another list comprehension.

Consider the following example of a 3x4 matrix implemented as a list of
3 lists of length 4:

```python
>>> matrix = [
... [1, 2, 3, 4],
... [5, 6, 7, 8],
... [9, 10, 11, 12],
... ]

```

The following list comprehension will transpose rows and columns:

```python
>>> [[row[i] for row in matrix] for i in range(4)]
[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

```

As we saw in the previous section, the inner list comprehension is evaluated in
the context of the `for` that follows it, so this example is
equivalent to:

```python
>>> transposed = []
>>> for i in range(4):
... transposed.append([row[i] for row in matrix])
...
>>> transposed
[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

```

which, in turn, is the same as:
