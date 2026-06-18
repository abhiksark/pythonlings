# Decorators

Source: https://docs.python.org/3/reference/compound_stmts.html#function-definitions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Decorators wrap or transform functions and classes with `@decorator` syntax.

## Extracted reference

8.7. Function definitions

A function definition defines a user-defined function object (see section
The standard type hierarchy):

```python

funcdef: [decorators] "def" funcname [type_params] "(" [parameter_list] ")"
["->" expression] ":" suite
decorators: decorator+
decorator: "@" assignment_expression NEWLINE
parameter_list: defparameter ("," defparameter)* "," "/" ["," [parameter_list_no_posonly]]
| parameter_list_no_posonly
parameter_list_no_posonly: defparameter ("," defparameter)* ["," [parameter_list_starargs]]
| parameter_list_starargs
parameter_list_starargs: "*" [star_parameter] ("," defparameter)* ["," [parameter_star_kwargs]]
| "*" ("," defparameter)+ ["," [parameter_star_kwargs]]
| parameter_star_kwargs
parameter_star_kwargs: "**" parameter [","]
parameter: identifier [":" expression]
star_parameter: identifier [":" ["*"] expression]
defparameter: parameter ["=" expression]
funcname: identifier

```

A function definition is an executable statement. Its execution binds the
function name in the current local namespace to a function object (a wrapper
around the executable code for the function). This function object contains a
reference to the current global namespace as the global namespace to be used
when the function is called.

The function definition does not execute the function body; this gets executed
only when the function is called. [4]

A function definition may be wrapped by one or more decorator expressions.
Decorator expressions are evaluated when the function is defined, in the scope
that contains the function definition. The result must be a callable, which is
invoked with the function object as the only argument. The returned value is
bound to the function name instead of the function object. Multiple decorators

## More reference

Source: https://docs.python.org/3/library/functools.html#functools.wraps

`functools.wraps` preserves the wrapped function's metadata.

@functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)

This is a convenience function for invoking `update_wrapper()` as a
function decorator when defining a wrapper function. It is equivalent to
`partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)`.
For example:

```python
>>> from functools import wraps
>>> def my_decorator(f):
... @wraps(f)
... def wrapper(*args, **kwds):
... print('Calling decorated function')
... return f(*args, **kwds)
... return wrapper
...
>>> @my_decorator
... def example():
... """Docstring"""
... print('Called example function')
...
>>> example()
Calling decorated function
Called example function
>>> example.__name__
'example'
>>> example.__doc__
'Docstring'

```

Without the use of this decorator factory, the name of the example function
would have been `'wrapper'`, and the docstring of the original `example()`
would have been lost.
