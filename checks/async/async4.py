# checks/async/async4.py
import asyncio

assert asyncio.run(collect()) == ["a", "b"], (
    "collect() should return ['a', 'b']"
)
print("async4 ok")
