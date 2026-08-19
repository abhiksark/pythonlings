import asyncio

assert asyncio.run(double_all([1, 2, 3])) == [2, 4, 6], "double_all() should return [2, 4, 6] for [1, 2, 3]"
print("async9 ok")
