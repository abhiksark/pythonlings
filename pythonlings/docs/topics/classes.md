# Classes

Source: https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Classes combine data and behavior into reusable types.

## Extracted reference

9.3. A First Look at Classes

Classes introduce a little bit of new syntax, three new object types, and some
new semantics.

9.3.1. Class Definition Syntax

The simplest form of class definition looks like this:

```python
class ClassName:
<statement-1>
.
.
.
<statement-N>

```

Class definitions, like function definitions (`def` statements) must be
executed before they have any effect. (You could conceivably place a class
definition in a branch of an `if` statement, or inside a function.)

In practice, the statements inside a class definition will usually be function
definitions, but other statements are allowed, and sometimes useful — we’ll
come back to this later. The function definitions inside a class normally have
a peculiar form of argument list, dictated by the calling conventions for
methods — again, this is explained later.

When a class definition is entered, a new namespace is created, and used as the
local scope — thus, all assignments to local variables go into this new
namespace. In particular, function definitions bind the name of the new
function here.

When a class definition is left normally (via the end), a class object is
created. This is basically a wrapper around the contents of the namespace
created by the class definition; we’ll learn more about class objects in the
next section. The original local scope (the one in effect just before the class
definition was entered) is reinstated, and the class object is bound here to the
class name given in the class definition header (`ClassName` in the

## More reference

Source: https://docs.python.org/3/reference/datamodel.html#special-method-names

Special methods like `__init__`, `__str__`, and `__repr__`.

3.3. Special method names

A class can implement certain operations that are invoked by special syntax
(such as arithmetic operations or subscripting and slicing) by defining methods
with special names. This is Python’s approach to operator overloading,
allowing classes to define their own behavior with respect to language
operators. For instance, if a class defines a method named
`__getitem__()`,
and `x` is an instance of this class, then `x[i]` is roughly equivalent
to `type(x).__getitem__(x, i)`. Except where mentioned, attempts to execute an
operation raise an exception when no appropriate method is defined (typically
`AttributeError` or `TypeError`).

Setting a special method to `None` indicates that the corresponding
operation is not available. For example, if a class sets
`__iter__()` to `None`, the class is not iterable, so calling
`iter()` on its instances will raise a `TypeError` (without
falling back to `__getitem__()`). [2]

When implementing a class that emulates any built-in type, it is important that
the emulation only be implemented to the degree that it makes sense for the
object being modelled. For example, some sequences may work well with retrieval
of individual elements, but extracting a slice may not make sense.
(One example of this is the NodeList interface
in the W3C’s Document Object Model.)

3.3.1. Basic customization

object.__new__(cls[, ...])

Called to create a new instance of class cls. `__new__()` is a static
method (special-cased so you need not declare it as such) that takes the class
of which an instance was requested as its first argument. The remaining
arguments are those passed to the object constructor expression (the call to the
class). The return value of `__new__()` should be the new object instance
(usually an instance of cls).

Typical implementations create a new instance of the class by invoking the
superclass’s `__new__()` method using `super().__new__(cls[, ...])`
with appropriate arguments and then modifying the newly created instance
