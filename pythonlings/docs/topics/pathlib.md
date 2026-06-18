# Pathlib

Source: https://docs.python.org/3/library/pathlib.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`pathlib.Path` represents filesystem paths with object-oriented helpers.

## Extracted reference

pathlib — Object-oriented filesystem paths — Python 3.14.6 documentation

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

- File and Directory Access »

- `pathlib` — Object-oriented filesystem paths

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir

`Path.mkdir` creates directories with parents/exist_ok options.

Path.mkdir(mode=0o777, parents=False, exist_ok=False)

Create a new directory at this given path. If mode is given, it is
combined with the process’s `umask` value to determine the file mode
and access flags. If the path already exists, `FileExistsError`
is raised.

If parents is true, any missing parents of this path are created
as needed; they are created with the default permissions without taking
mode into account (mimicking the POSIX `mkdir -p` command).

If parents is false (the default), a missing parent raises
`FileNotFoundError`.

If exist_ok is false (the default), `FileExistsError` is
raised if the target directory already exists.

If exist_ok is true, `FileExistsError` will not be raised unless the given
path already exists in the file system and is not a directory (same
behavior as the POSIX `mkdir -p` command).

Changed in version 3.5: The exist_ok parameter was added.
