import asyncio

assert asyncio.run(with_timeout()) == "done", "with_timeout() should return 'done' within the timeout"
print("async7 ok")
