"""
Module for handling CAMUNDA tasks.
"""
import asyncio
import logging

from pathlib import Path

from pyzeebe import ZeebeWorker, Job, create_insecure_channel

from ticket_broker.route_database import RouteDatabase

rdb = RouteDatabase.from_file(Path("data/railways.yaml"))


async def run_worker():
    print("Creating ticket_broker worker")
    channel = create_insecure_channel()
    worker = ZeebeWorker(channel)

    @worker.task(task_type="find_route")
    async def find_route(start_station: str, end_station: str, ticket_class: str):
        """
        Finds routes based on input
        """
        print("Received find_route request")
        return {"routes": [
            {
                "legs": [
                    {"from": "A",
                     "to": "B"},
                    {"from": "B",
                     "to": "C"}
                ]
            }
        ]}

    await worker.work()
