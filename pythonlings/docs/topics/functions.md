# Functions

Source: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`def` creates reusable behavior with parameters, return values, and optional defaults.

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

Source: https://docs.python.org/3/reference/compound_stmts.html#function-definitions

Function definition syntax including parameters, annotations, and decorators.

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
