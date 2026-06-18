# File I/O

Source: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`open` and `with` are the usual tools for reading and writing files safely.

## Extracted reference

7.2. Reading and Writing Files

`open()` returns a file object, and is most commonly used with
two positional arguments and one keyword argument:
`open(filename, mode, encoding=None)`

```python
>>> f = open('workfile', 'w', encoding="utf-8")

```

The first argument is a string containing the filename. The second argument is
another string containing a few characters describing the way in which the file
will be used. mode can be `'r'` when the file will only be read, `'w'`
for only writing (an existing file with the same name will be erased), and
`'a'` opens the file for appending; any data written to the file is
automatically added to the end. `'r+'` opens the file for both reading and
writing. The mode argument is optional; `'r'` will be assumed if it’s
omitted.

Normally, files are opened in text mode, that means, you read and write
strings from and to the file, which are encoded in a specific encoding.
If encoding is not specified, the default is platform dependent
(see `open()`).
Because UTF-8 is the modern de-facto standard, `encoding="utf-8"` is
recommended unless you know that you need to use a different encoding.
Appending a `'b'` to the mode opens the file in binary mode.
Binary mode data is read and written as `bytes` objects.
You can not specify encoding when opening file in binary mode.

In text mode, the default when reading is to convert platform-specific line
endings (`\n` on Unix, `\r\n` on Windows) to just `\n`. When writing in
text mode, the default is to convert occurrences of `\n` back to
platform-specific line endings. This behind-the-scenes modification
to file data is fine for text files, but will corrupt binary data like that in
`JPEG` or `EXE` files. Be very careful to use binary mode when
reading and writing such files.

It is good practice to use the `with` keyword when dealing
with file objects. The advantage is that the file is properly closed

## More reference

Source: https://docs.python.org/3/library/io.html#high-level-module-interface

The high-level `open()` interface and its modes.

High-level Module Interface

io.DEFAULT_BUFFER_SIZE

An int containing the default buffer size used by the module’s buffered I/O
classes. `open()` uses the file’s blksize (as obtained by
`os.stat()`) if possible.

io.open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

This is an alias for the builtin `open()` function.

This function raises an auditing event `open` with
arguments path, mode and flags. The mode and flags
arguments may have been modified or inferred from the original call.

io.open_code(path)

Opens the provided file with mode `'rb'`. This function should be used
when the intent is to treat the contents as executable code.

path should be a `str` and an absolute path.

The behavior of this function may be overridden by an earlier call to the
`PyFile_SetOpenCodeHook()`. However, assuming that path is a
`str` and an absolute path, `open_code(path)` should always behave
the same as `open(path, 'rb')`. Overriding the behavior is intended for
additional validation or preprocessing of the file.

Added in version 3.8.

io.text_encoding(encoding, stacklevel=2, /)

This is a helper function for callables that use `open()` or
`TextIOWrapper` and have an `encoding=None` parameter.

This function returns encoding if it is not `None`.
Otherwise, it returns `"locale"` or `"utf-8"` depending on
UTF-8 Mode.
