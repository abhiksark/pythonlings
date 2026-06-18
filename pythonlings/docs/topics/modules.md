# Modules

Source: https://docs.python.org/3/tutorial/modules.html#modules

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Modules organize Python code into importable files and packages.

## Extracted reference

6. Modules

If you quit from the Python interpreter and enter it again, the definitions you
have made (functions and variables) are lost. Therefore, if you want to write a
somewhat longer program, you are better off using a text editor to prepare the
input for the interpreter and running it with that file as input instead. This
is known as creating a script. As your program gets longer, you may want to
split it into several files for easier maintenance. You may also want to use a
handy function that you’ve written in several programs without copying its
definition into each program.

To support this, Python has a way to put definitions in a file and use them in a
script or in an interactive instance of the interpreter. Such a file is called a
module; definitions from a module can be imported into other modules or into
the main module (the collection of variables that you have access to in a
script executed at the top level and in calculator mode).

A module is a file containing Python definitions and statements. The file name
is the module name with the suffix `.py` appended. Within a module, the
module’s name (as a string) is available as the value of the global variable
`__name__`. For instance, use your favorite text editor to create a file
called `fibo.py` in the current directory with the following contents:

```python
# Fibonacci numbers module

def fib(n):
"""Write Fibonacci series up to n."""
a, b = 0, 1
while a < n:
print(a, end=' ')
a, b = b, a+b
print()

def fib2(n):
"""Return Fibonacci series up to n."""
result = []
a, b = 0, 1
while a < n:
result.append(a)

## More reference

Source: https://docs.python.org/3/library/importlib.html#importlib.reload

Reloading and dynamically importing modules with importlib.

importlib.reload(module)

Reload a previously imported module. The argument must be a module object,
so it must have been successfully imported before. This is useful if you
have edited the module source file using an external editor and want to try
out the new version without leaving the Python interpreter. The return value
is the module object (which can be different if re-importing causes a
different object to be placed in `sys.modules`).

When `reload()` is executed:

-

Python module’s code is recompiled and the module-level code re-executed,
defining a new set of objects which are bound to names in the module’s
dictionary by reusing the loader which originally loaded the
module. The `init` function of extension modules is not called a second
time.

-

As with all other objects in Python the old objects are only reclaimed
after their reference counts drop to zero.

-

The names in the module namespace are updated to point to any new or
changed objects.

-

Other references to the old objects (such as names external to the module) are
not rebound to refer to the new objects and must be updated in each namespace
where they occur if that is desired.

There are a number of other caveats:

When a module is reloaded, its dictionary (containing the module’s global
variables) is retained. Redefinitions of names will override the old
definitions, so this is generally not a problem. If the new version of a
