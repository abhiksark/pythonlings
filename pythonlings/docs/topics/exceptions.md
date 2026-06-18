# Exceptions

Source: https://docs.python.org/3/tutorial/errors.html#handling-exceptions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`try` and `except` handle errors without crashing the whole program.

## Extracted reference

8.3. Handling Exceptions

It is possible to write programs that handle selected exceptions. Look at the
following example, which asks the user for input until a valid integer has been
entered, but allows the user to interrupt the program (using Control-C or
whatever the operating system supports); note that a user-generated interruption
is signalled by raising the `KeyboardInterrupt` exception.

```python
>>> while True:
... try:
... x = int(input("Please enter a number: "))
... break
... except ValueError:
... print("Oops! That was no valid number. Try again...")
...

```

The `try` statement works as follows.

-

First, the try clause (the statement(s) between the `try` and
`except` keywords) is executed.

-

If no exception occurs, the except clause is skipped and execution of the
`try` statement is finished.

-

If an exception occurs during execution of the `try` clause, the rest of the
clause is skipped. Then, if its type matches the exception named after the
`except` keyword, the except clause is executed, and then execution
continues after the try/except block.

-

## More reference

Source: https://docs.python.org/3/library/exceptions.html#concrete-exceptions

Concrete built-in exceptions like ValueError, KeyError, and TypeError.

Concrete exceptions

The following exceptions are the exceptions that are usually raised.

exception AssertionError

Raised when an `assert` statement fails.

exception AttributeError

Raised when an attribute reference (see Attribute references) or
assignment fails. (When an object does not support attribute references or
attribute assignments at all, `TypeError` is raised.)

The optional name and obj keyword-only arguments
set the corresponding attributes:

name

The name of the attribute that was attempted to be accessed.

obj

The object that was accessed for the named attribute.

Changed in version 3.10: Added the `name` and `obj` attributes.

exception EOFError

Raised when the `input()` function hits an end-of-file condition (EOF)
without reading any data. (Note: the `io.TextIOBase.read()` and
`io.IOBase.readline()` methods return an empty string when they hit EOF.)

exception FloatingPointError

Not currently used.

exception GeneratorExit

Raised when a generator or coroutine is closed;
