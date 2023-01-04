"""
Module for handling CAMUNDA tasks.
"""
import asyncio

from ticket_broker.worker_instance import WorkerInstance

WorkerInstance()

from ticket_broker.use_cases import *

def run_loop():
    worker, _ = WorkerInstance.get()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.work())
