import asyncio

from ticket_broker.worker import run_worker

asyncio.run(run_worker())
