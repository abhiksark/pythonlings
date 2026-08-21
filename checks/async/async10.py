# checks/async/async10.py
import asyncio

assert asyncio.run(fetch_all(["ada", "lin", "guido"])) == "ADA,LIN,GUIDO", (
    "fetch_all() should return the names uppercased and comma-separated"
)
print("async10 ok")
