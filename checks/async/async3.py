# checks/async/async3.py
import asyncio

assert asyncio.run(wake_up()) == "awake", (
    "wake_up() should return 'awake'"
)
print("async3 ok")
