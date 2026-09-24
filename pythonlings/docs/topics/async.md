# Asyncio

Source: https://docs.python.org/3/library/asyncio.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`asyncio` runs concurrent I/O-bound work with coroutines and an event loop.

## Extracted reference

asyncio — Asynchronous I/O — Python 3.14.6 documentation

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

- Networking and Interprocess Communication »

- `asyncio` — Asynchronous I/O

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/asyncio-task.html#coroutines

Coroutines and `async`/`await` with execution examples.

Coroutines

Source code: Lib/asyncio/coroutines.py

Coroutines declared with the async/await syntax is the
preferred way of writing asyncio applications. For example, the following
snippet of code prints “hello”, waits 1 second,
and then prints “world”:

```python
>>> import asyncio

>>> async def main():
... print('hello')
... await asyncio.sleep(1)
... print('world')

>>> asyncio.run(main())
hello
world

```

Note that simply calling a coroutine will not schedule it to
be executed:

```python
>>> main()
<coroutine object main at 0x1053bb7c8>

```

To actually run a coroutine, asyncio provides the following mechanisms:

-

The `asyncio.run()` function to run the top-level
entry point “main()” function (see the above example.)

-
