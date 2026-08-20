# checks/async/async5.py
import asyncio

assert asyncio.run(run_task()) == 42, (
    "run_task() should return 42"
)
print("async5 ok")
