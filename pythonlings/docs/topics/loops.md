# Loops

Source: https://docs.python.org/3/tutorial/controlflow.html#for-statements

This local reference is generated from the official Python documentation and trimmed for pythonlings.

`for` loops iterate over items; `while` loops continue while a condition is true.

## Extracted reference

4.2. `for` Statements

The `for` statement in Python differs a bit from what you may be used
to in C or Pascal. Rather than always iterating over an arithmetic progression
of numbers (like in Pascal), or giving the user the ability to define both the
iteration step and halting condition (as C), Python’s `for` statement
iterates over the items of any sequence (a list or a string), in the order that
they appear in the sequence. For example (no pun intended):

```python
>>> # Measure some strings:
>>> words = ['cat', 'window', 'defenestrate']
>>> for w in words:
... print(w, len(w))
...
cat 3
window 6
defenestrate 12

```

Code that modifies a collection while iterating over that same collection can
be tricky to get right. Instead, it is usually more straight-forward to loop
over a copy of the collection or to create a new collection:

```python
# Create a sample collection
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# Strategy: Iterate over a copy
for user, status in users.copy().items():
if status == 'inactive':
del users[user]

# Strategy: Create a new collection
active_users = {}
for user, status in users.items():
if status == 'active':
active_users[user] = status

## More reference

Source: https://docs.python.org/3/reference/compound_stmts.html#the-for-statement

Formal for-statement syntax and iteration semantics.

8.3. The `for` statement

The `for` statement is used to iterate over the elements of a sequence
(such as a string, tuple or list) or other iterable object:

```python

for_stmt: "for" target_list "in" starred_expression_list ":" suite
["else" ":" suite]

```

The `starred_expression_list` expression is evaluated
once; it should yield an iterable object. An iterator is
created for that iterable. The first item provided by the iterator is then
assigned to the target list using the standard rules for assignments
(see Assignment statements), and the suite is executed. This repeats for each
item provided by the iterator. When the iterator is exhausted,
the suite in the `else` clause,
if present, is executed, and the loop terminates.

A `break` statement executed in the first suite terminates the loop
without executing the `else` clause’s suite. A `continue`
statement executed in the first suite skips the rest of the suite and continues
with the next item, or with the `else` clause if there is no next
item.

The for-loop makes assignments to the variables in the target list.
This overwrites all previous assignments to those variables including
those made in the suite of the for-loop:

```python
for i in range(10):
print(i)
i = 5 # this will not affect the for-loop
# because i will be overwritten with the next
# index in the range

```
