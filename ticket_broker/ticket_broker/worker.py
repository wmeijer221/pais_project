"""
Module for handling CAMUNDA tasks.
"""
import asyncio
import logging
import uuid

from typing import Dict
from pathlib import Path

from pyzeebe import ZeebeWorker, Job, create_insecure_channel, ZeebeTaskRouter, ZeebeClient, SyncZeebeClient

from ticket_broker.route_database import RouteDatabase

rdb = RouteDatabase.from_file(Path("data/railways.yaml"))

print("Creating ticket_broker worker")
channel = create_insecure_channel()
worker = ZeebeWorker(channel)
client = ZeebeClient(channel)


@worker.task(task_type="send_journey_specification")
async def send_journey_specification(journey_specification: Dict, order_id: str):
    """
    Sends the message to initialise the broker pool.
    """
    print(f"Received job: send_journey_specification : {journey_specification}")

    message = {
        "order_id": order_id,
        "journey_specification": journey_specification
    }

    print("publishing message to ticket broker")
    await client.publish_message("find_journey", str(order_id), message)


@worker.task(task_type="find_route_options")
async def find_route_options(journey_specification: Dict, order_id: str):
    """
    Finds route options and sends it to the customer.
    """
    print(f"Received job: find_route_options : {journey_specification} {order_id}")

    if journey_specification['class'] == "first":
        weight = 'price_eurocents_firstclass'
    else:
        weight = 'price_eurocents_economy'

    options = rdb.find_route_options(journey_specification['start_station'],
                                     journey_specification['end_station'],
                                     weight)

    message = {"route_options": options}
    await client.publish_message("receive_journey_options", str(order_id), message)

    return message


def run_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.work())
