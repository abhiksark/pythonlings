# Type Hints

Source: https://docs.python.org/3/library/typing.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Type hints annotate expected values and help tools reason about your code.

## Extracted reference

typing — Support for type hints — Python 3.14.6 documentation

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

- `typing` — Support for type hints

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/reference/datamodel.html#annotations

How annotations are stored in `__annotations__`.

3.3.12. Annotations

Functions, classes, and modules may contain annotations,
which are a way to associate information (usually type hints)
with a symbol.

object.__annotations__

This attribute contains the annotations for an object. It is
lazily evaluated, so accessing the attribute may
execute arbitrary code and raise exceptions. If evaluation is successful, the
attribute is set to a dictionary mapping from variable names to annotations.

Changed in version 3.14: Annotations are now lazily evaluated.

object.__annotate__(format)

An annotate function.
Returns a new dictionary object mapping attribute/parameter names to their annotation values.

Takes a format parameter specifying the format in which annotations values should be provided.
It must be a member of the `annotationlib.Format` enum, or an integer with
a value corresponding to a member of the enum.

If an annotate function doesn’t support the requested format, it must raise
`NotImplementedError`. Annotate functions must always support
`VALUE` format; they must not raise
`NotImplementedError()` when called with this format.

When called with `VALUE` format, an annotate function may raise
`NameError`; it must not raise `NameError` when called requesting any other format.

If an object does not have any annotations, `__annotate__` should preferably be set
to `None` (it can’t be deleted), rather than set to a function that returns an empty dict.

Added in version 3.14.

See also

PEP 649 — Deferred evaluation of annotation using descriptors
