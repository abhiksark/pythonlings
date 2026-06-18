# Variables

Source: https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Assigning names with `=` lets you keep values for later expressions.

## Extracted reference

3.1. Using Python as a Calculator

Let’s try some simple Python commands. Start the interpreter and wait for the
primary prompt, `>>>`. (It shouldn’t take long.)

3.1.1. Numbers

The interpreter acts as a simple calculator: you can type an expression into it
and it will write the value. Expression syntax is straightforward: the
operators `+`, `-`, `*` and `/` can be used to perform
arithmetic; parentheses (`()`) can be used for grouping.
For example:

```python
>>> 2 + 2
4
>>> 50 - 5*6
20
>>> (50 - 5*6) / 4
5.0
>>> 8 / 5 # division always returns a floating-point number
1.6

```

The integer numbers (e.g. `2`, `4`, `20`) have type `int`,
the ones with a fractional part (e.g. `5.0`, `1.6`) have type
`float`. We will see more about numeric types later in the tutorial.

Division (`/`) always returns a float. To do floor division and
get an integer result you can use the `//` operator; to calculate
the remainder you can use `%`:

```python
>>> 17 / 3 # classic division returns a float
5.666666666666667
>>>
>>> 17 // 3 # floor division discards the fractional part
5
>>> 17 % 3 # the % operator returns the remainder of the division

## More reference

Source: https://docs.python.org/3/reference/simple_stmts.html#assignment-statements

Assignment statement syntax and semantics, including multiple and unpacking targets.

7.2. Assignment statements

Assignment statements are used to (re)bind names to values and to modify
attributes or items of mutable objects:

```python

assignment_stmt: (target_list "=")+ (starred_expression | yield_expression)
target_list: target ("," target)* [","]
target: identifier
| "(" [target_list] ")"
| "[" [target_list] "]"
| attributeref
| subscription
| "*" target

```

(See section Primaries for the syntax definitions for attributeref
and subscription.)

An assignment statement evaluates the expression list (remember that this can be
a single expression or a comma-separated list, the latter yielding a tuple) and
assigns the single resulting object to each of the target lists, from left to
right.

Assignment is defined recursively depending on the form of the target (list).
When a target is part of a mutable object (an attribute reference or
subscription), the mutable object must ultimately perform the assignment and
decide about its validity, and may raise an exception if the assignment is
unacceptable. The rules observed by various types and the exceptions raised are
given with the definition of the object types (see section The standard type hierarchy).

Assignment of an object to a target list, optionally enclosed in parentheses or
square brackets, is recursively defined as follows.

-

If the target list is a single target with no trailing comma,
optionally in parentheses, the object is assigned to that target.
