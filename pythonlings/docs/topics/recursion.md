# Recursion

Source: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Recursive functions solve a problem by calling themselves on smaller inputs.

## Extracted reference

4.8. Defining Functions

We can create a function that writes the Fibonacci series to an arbitrary
boundary:

```python
>>> def fib(n): # write Fibonacci series less than n
... """Print a Fibonacci series less than n."""
... a, b = 0, 1
... while a < n:
... print(a, end=' ')
... a, b = b, a+b
... print()
...
>>> # Now call the function we just defined:
>>> fib(2000)
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

```

The keyword `def` introduces a function definition. It must be
followed by the function name and the parenthesized list of formal parameters.
The statements that form the body of the function start at the next line, and
must be indented.

The first statement of the function body can optionally be a string literal;
this string literal is the function’s documentation string, or docstring.
(More about docstrings can be found in the section Documentation Strings.)
There are tools which use docstrings to automatically produce online or printed
documentation, or to let the user interactively browse through code; it’s good
practice to include docstrings in code that you write, so make a habit of it.

The execution of a function introduces a new symbol table used for the local
variables of the function. More precisely, all variable assignments in a
function store the value in the local symbol table; whereas variable references
first look in the local symbol table, then in the local symbol tables of
enclosing functions, then in the global symbol table, and finally in the table
of built-in names. Thus, global variables and variables of enclosing functions
cannot be directly assigned a value within a function (unless, for global
variables, named in a `global` statement, or, for variables of enclosing

## More reference

Source: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit

Adjusting the interpreter's recursion limit with `sys.setrecursionlimit`.

sys.setrecursionlimit(limit)

Set the maximum depth of the Python interpreter stack to limit. This limit
prevents infinite recursion from causing an overflow of the C stack and crashing
Python.

The highest possible limit is platform-dependent. A user may need to set the
limit higher when they have a program that requires deep recursion and a platform
that supports a higher limit. This should be done with care, because a too-high
limit can lead to a crash.

If the new limit is too low at the current recursion depth, a
`RecursionError` exception is raised.

Changed in version 3.5.1: A `RecursionError` exception is now raised if the new limit is too
low at the current recursion depth.
