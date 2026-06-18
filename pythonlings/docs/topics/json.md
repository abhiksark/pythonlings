# JSON

Source: https://docs.python.org/3/library/json.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`json` converts between Python values and JSON text.

## Extracted reference

json — JSON encoder and decoder — Python 3.14.6 documentation

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

- Internet Data Handling »

- `json` — JSON encoder and decoder

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/tutorial/inputoutput.html#saving-structured-data-with-json

Tutorial on saving and loading structured data as JSON.

7.2.2. Saving structured data with `json`

Strings can easily be written to and read from a file. Numbers take a bit more
effort, since the `read()` method only returns strings, which will have to
be passed to a function like `int()`, which takes a string like `'123'`
and returns its numeric value 123. When you want to save more complex data
types like nested lists and dictionaries, parsing and serializing by hand
becomes complicated.

Rather than having users constantly writing and debugging code to save
complicated data types to files, Python allows you to use the popular data
interchange format called JSON (JavaScript Object Notation). The standard module called `json` can take Python
data hierarchies, and convert them to string representations; this process is
called serializing. Reconstructing the data from the string representation
is called deserializing. Between serializing and deserializing, the
string representing the object may have been stored in a file or data, or
sent over a network connection to some distant machine.

Note

The JSON format is commonly used by modern applications to allow for data
exchange. Many programmers are already familiar with it, which makes
it a good choice for interoperability.

If you have an object `x`, you can view its JSON string representation with a
simple line of code:

```python
>>> import json
>>> x = [1, 'simple', 'list']
>>> json.dumps(x)
'[1, "simple", "list"]'

```

Another variant of the `dumps()` function, called `dump()`,
simply serializes the object to a text file. So if `f` is a
text file object opened for writing, we can do this:

```python
