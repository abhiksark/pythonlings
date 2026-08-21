# checks/async/async1.py
import asyncio

assert asyncio.run(greet()) == "hello async", (
    "greet() should return 'hello async'"
)
print("async1 ok")
