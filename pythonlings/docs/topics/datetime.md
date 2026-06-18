# Datetime

Source: https://docs.python.org/3/library/datetime.html

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`datetime` represents dates, times, durations, and time zones.

## Extracted reference

datetime — Basic date and time types — Python 3.14.6 documentation

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

- Data Types »

- `datetime` — Basic date and time types

-

|

-

Theme

## More reference

Source: https://docs.python.org/3/library/datetime.html#examples-of-usage-datetime

Worked `datetime` examples beyond the API reference.

Examples of usage: `datetime`

Examples of working with `datetime` objects:

```python
>>> import datetime as dt

>>> # Using datetime.combine()
>>> d = dt.date(2005, 7, 14)
>>> t = dt.time(12, 30)
>>> dt.datetime.combine(d, t)
datetime.datetime(2005, 7, 14, 12, 30)

>>> # Using datetime.now()
>>> dt.datetime.now()
datetime.datetime(2007, 12, 6, 16, 29, 43, 79043) # GMT +1
>>> dt.datetime.now(dt.timezone.utc)
datetime.datetime(2007, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)

>>> # Using datetime.strptime()
>>> my_datetime = dt.datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
>>> my_datetime
datetime.datetime(2006, 11, 21, 16, 30)

>>> # Using datetime.timetuple() to get tuple of all attributes
>>> tt = my_datetime.timetuple()
>>> for it in tt:
... print(it)
...
2006 # year
11 # month
21 # day
16 # hour
30 # minute
0 # second
1 # weekday (0 = Monday)
325 # number of days since 1st January
-1 # dst - method tzinfo.dst() returned None

>>> # Date in ISO format
