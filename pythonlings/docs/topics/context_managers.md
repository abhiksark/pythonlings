# Context Managers

Source: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Context managers run setup and cleanup around a block using `with`.

## Extracted reference

8.5. The `with` statement

The `with` statement is used to wrap the execution of a block with
methods defined by a context manager (see section With Statement Context Managers).
This allows common `try`…`except`…`finally`
usage patterns to be encapsulated for convenient reuse.

```python

with_stmt: "with" ( "(" with_stmt_contents ","? ")" | with_stmt_contents ) ":" suite
with_stmt_contents: with_item ("," with_item)*
with_item: expression ["as" target]

```

The execution of the `with` statement with one “item” proceeds as follows:

-

The context expression (the expression given in the
`with_item`) is evaluated to obtain a context manager.

-

The context manager’s `__enter__()` is loaded for later use.

-

The context manager’s `__exit__()` is loaded for later use.

-

The context manager’s `__enter__()` method is invoked.

-

If a target was included in the `with` statement, the return value
from `__enter__()` is assigned to it.

Note

## More reference

Source: https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager

`contextlib.contextmanager` builds a context manager from a generator.

@contextlib.contextmanager

This function is a decorator that can be used to define a factory
function for `with` statement context managers, without needing to
create a class or separate `__enter__()` and `__exit__()` methods.

While many objects natively support use in with statements, sometimes a
resource needs to be managed that isn’t a context manager in its own right,
and doesn’t implement a `close()` method for use with `contextlib.closing`.

An abstract example would be the following to ensure correct resource
management:

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
# Code to acquire resource, e.g.:
resource = acquire_resource(*args, **kwds)
try:
yield resource
finally:
# Code to release resource, e.g.:
release_resource(resource)

```

The function can then be used like this:

```python
>>> with managed_resource(timeout=3600) as resource:
... # Resource is released at the end of this block,
... # even if code in the block raises an exception

```

The function being decorated must return a generator-iterator when
called. This iterator must yield exactly one value, which will be bound to
the targets in the `with` statement’s `as` clause, if any.
