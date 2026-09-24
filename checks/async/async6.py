# checks/async/async6.py
import asyncio

assert asyncio.run(collect_numbers()) == [1, 2, 3], (
    "collect_numbers() should return [1, 2, 3]"
)
print("async6 ok")
