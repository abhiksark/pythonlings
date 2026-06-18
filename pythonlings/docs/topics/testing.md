# Testing

Source: https://docs.python.org/3/library/unittest.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Tests encode expected behavior so code can be checked repeatedly.

## Extracted reference

unittest — Unit testing framework — Python 3.14.6 documentation

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

- Development Tools »

- `unittest` — Unit testing framework

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/doctest.html#how-it-works

How doctest finds and runs examples embedded in docstrings.

How It Works

This section examines in detail how doctest works: which docstrings it looks at,
how it finds interactive examples, what execution context it uses, how it
handles exceptions, and how option flags can be used to control its behavior.
This is the information that you need to know to write doctest examples; for
information about actually running doctest on these examples, see the following
sections.

Which Docstrings Are Examined?

The module docstring, and all function, class and method docstrings are
searched. Objects imported into the module are not searched.

In addition, there are cases when you want tests to be part of a module but not part
of the help text, which requires that the tests not be included in the docstring.
Doctest looks for a module-level variable called `__test__` and uses it to locate other
tests. If `M.__test__` exists, it must be a dict, and each
entry maps a (string) name to a function object, class object, or string.
Function and class object docstrings found from `M.__test__` are searched, and
strings are treated as if they were docstrings. In output, a key `K` in
`M.__test__` appears with name `M.__test__.K`.

For example, place this block of code at the top of `example.py`:

```python
__test__ = {
'numbers': """
>>> factorial(6)
720

>>> [factorial(n) for n in range(6)]
[1, 1, 2, 6, 24, 120]
"""
}

```

The value of `example.__test__["numbers"]` will be treated as a
docstring and all the tests inside it will be run. It is
