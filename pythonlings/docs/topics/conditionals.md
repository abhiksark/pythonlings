# Conditionals

Source: https://docs.python.org/3/tutorial/controlflow.html#if-statements

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`if`, `elif`, and `else` choose which block runs based on boolean conditions.

## Extracted reference

4.1. `if` Statements

Perhaps the most well-known statement type is the `if` statement. For
example:

```python
>>> x = int(input("Please enter an integer: "))
Please enter an integer: 42
>>> if x < 0:
... x = 0
... print('Negative changed to zero')
... elif x == 0:
... print('Zero')
... elif x == 1:
... print('Single')
... else:
... print('More')
...
More

```

There can be zero or more `elif` parts, and the `else` part is
optional. The keyword ‘`elif`’ is short for ‘else if’, and is useful
to avoid excessive indentation. An `if` … `elif` …
`elif` … sequence is a substitute for the `switch` or
`case` statements found in other languages.

If you’re comparing the same value to several constants, or checking for specific types or
attributes, you may also find the `match` statement useful. For more
details see match Statements.

## More reference

Source: https://docs.python.org/3/tutorial/controlflow.html#match-statements

`match` pattern matching with examples and syntax.

4.7. `match` Statements

A `match` statement takes an expression and compares its value to successive
patterns given as one or more case blocks. This is superficially
similar to a switch statement in C, Java or JavaScript (and many
other languages), but it’s more similar to pattern matching in
languages like Rust or Haskell. Only the first pattern that matches
gets executed and it can also extract components (sequence elements
or object attributes) from the value into variables. If no case matches,
none of the branches is executed.

The simplest form compares a subject value against one or more literals:

```python
def http_error(status):
match status:
case 400:
return "Bad request"
case 404:
return "Not found"
case 418:
return "I'm a teapot"
case _:
return "Something's wrong with the internet"

```

Note the last block: the “variable name” `_` acts as a wildcard and
never fails to match.

You can combine several literals in a single pattern using `|` (“or”):

```python
case 401 | 403 | 404:
return "Not allowed"

```

Patterns can look like unpacking assignments, and can be used to bind
variables:
