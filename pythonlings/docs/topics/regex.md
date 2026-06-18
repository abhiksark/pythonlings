# Regular Expressions

Source: https://docs.python.org/3/library/re.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

The `re` module searches, matches, and transforms text using regular expressions.

## Extracted reference

re — Regular expression operations — Python 3.14.6 documentation

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

- Text Processing Services »

- `re` — Regular expression operations

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/howto/regex.html#search-and-replace

Practical search-and-replace patterns from the regex HOWTO.

Search and replace

Another common task is to find all the matches for a pattern, and replace them
with a different string. The `sub()` method takes a replacement value,
which can be either a string or a function, and the string to be processed.

.sub(replacement, string[, count=0])

Returns the string obtained by replacing the leftmost non-overlapping
occurrences of the RE in string by the replacement replacement. If the
pattern isn’t found, string is returned unchanged.

The optional argument count is the maximum number of pattern occurrences to be
replaced; count must be a non-negative integer. The default value of 0 means
to replace all occurrences.

Here’s a simple example of using the `sub()` method. It replaces colour
names with the word `colour`:

```python
>>> p = re.compile('(blue|white|red)')
>>> p.sub('colour', 'blue socks and red shoes')
'colour socks and colour shoes'
>>> p.sub('colour', 'blue socks and red shoes', count=1)
'colour socks and red shoes'

```

The `subn()` method does the same work, but returns a 2-tuple containing the
new string value and the number of replacements that were performed:

```python
>>> p = re.compile('(blue|white|red)')
>>> p.subn('colour', 'blue socks and red shoes')
('colour socks and colour shoes', 2)
>>> p.subn('colour', 'no colours at all')
('no colours at all', 0)

```
