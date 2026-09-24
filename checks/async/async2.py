# checks/async/async2.py
import asyncio

assert asyncio.run(main()) == "ready", (
    "main() should return 'ready'"
)
print("async2 ok")
