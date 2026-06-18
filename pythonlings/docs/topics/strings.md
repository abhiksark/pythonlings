# Strings

Source: https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Strings are immutable text sequences with indexing, slicing, and many useful methods.

## Extracted reference

Text Sequence Type — `str`

Textual data in Python is handled with `str` objects, or strings.
Strings are immutable
sequences of Unicode code points. String literals are
written in a variety of ways:

-

Single quotes: `'allows embedded "double" quotes'`

-

Double quotes: `"allows embedded 'single' quotes"`

-

Triple quoted: `'''Three single quotes'''`, `"""Three double quotes"""`

Triple quoted strings may span multiple lines - all associated whitespace will
be included in the string literal.

String literals that are part of a single expression and have only whitespace
between them will be implicitly converted to a single string literal. That
is, `("spam " "eggs") == "spam eggs"`.

See String and Bytes literals for more about the various forms of string literal,
including supported escape sequences, and the `r` (“raw”) prefix that
disables most escape sequence processing.

Strings may also be created from other objects using the `str`
constructor.

Since there is no separate “character” type, indexing a string produces
strings of length 1. That is, for a non-empty string s, `s[0] == s[0:1]`.

There is also no mutable string type, but `str.join()` or
`io.StringIO` can be used to efficiently construct strings from
multiple fragments.

## More reference

Source: https://docs.python.org/3/library/stdtypes.html#string-methods

Full reference of string methods with signatures and behaviors.

String Methods

Strings implement all of the common sequence
operations, along with the additional methods described below.

Strings also support two styles of string formatting, one providing a large
degree of flexibility and customization (see `str.format()`,
Format string syntax and Custom string formatting) and the other based on C
`printf` style formatting that handles a narrower range of types and is
slightly harder to use correctly, but is often faster for the cases it can
handle (printf-style String Formatting).

The Text Processing Services section of the standard library covers a number of
other modules that provide various text related utilities (including regular
expression support in the `re` module).

str.capitalize()

Return a copy of the string with its first character capitalized and the
rest lowercased.

Changed in version 3.8: The first character is now put into titlecase rather than uppercase.
This means that characters like digraphs will only have their first
letter capitalized, instead of the full character.

str.casefold()

Return a casefolded copy of the string. Casefolded strings may be used for
caseless matching.

Casefolding is similar to lowercasing but more aggressive because it is
intended to remove all case distinctions in a string. For example, the German
lowercase letter `'ß'` is equivalent to `"ss"`. Since it is already
lowercase, `lower()` would do nothing to `'ß'`; `casefold()`
converts it to `"ss"`.
For example:

```python
>>> 'straße'.lower()
'straße'
