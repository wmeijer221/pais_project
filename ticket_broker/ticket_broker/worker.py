"""
Module for handling CAMUNDA tasks.
"""
import asyncio
import json
import logging
import os
import uuid

from typing import Dict
from pathlib import Path

from pyzeebe import ZeebeWorker, Job, create_insecure_channel, ZeebeTaskRouter, ZeebeClient, SyncZeebeClient

from ticket_broker.route_database import RouteDatabase
from ticket_broker.journey_booker import JourneyBooker
from ticket_broker.bank_verifier import BankVerifier

rdb = RouteDatabase.from_file(Path("data/railways.yaml"))
jb = JourneyBooker()
bf = BankVerifier()

if "ENDPOINT_HOST" in os.environ.keys() and "ENDPOINT_PORT" in os.environ.keys():
    channel = create_insecure_channel(
        hostname=os.environ["ENDPOINT_HOST"], port=int(os.environ["ENDPOINT_PORT"]))
else:
    logging.warning("No endpoint specified. Using defaults!")
    channel = create_insecure_channel()

print("Creating ticket_broker worker")
worker = ZeebeWorker(channel)
client = ZeebeClient(channel)

async def example_logging_task_decorator(job: Job) -> Job:
    logging.debug(f'\nReceived job {job.type} ({job.key})\n')
    return job

async def on_error(exception: Exception, job: Job):
    """Basic error handler."""
    status = f"Failed to handle job {job}. Error: {str(exception)}"
    logging.warning(status)
    job.set_error_status(status)


@worker.task(task_type="send_journey_specification", before=[example_logging_task_decorator])
async def send_journey_specification(journey_specification: Dict, order_id: str):
    """
    Sends the message to initialise the broker pool.
    """

    message = {
        "order_id": order_id,
        "journey_specification": journey_specification
    }

    await client.publish_message("find_journey", str(order_id), message)


@worker.task(task_type="find_route_options", before=[example_logging_task_decorator])
async def find_route_options(journey_specification: Dict, order_id: str):
    """
    Finds route options and sends it to the customer.
    """

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


@worker.task(task_type="send_order_placement", before=[example_logging_task_decorator])
async def send_order_placement(billing_information: Dict, option_selected_id: str, order_id: str):
    message = {
        "billing_information": billing_information,
        "option_selected_id": option_selected_id,
        "order_id": order_id
    }
    await client.publish_message("place_order", str(order_id), message)


@worker.task(task_type="place_order", exception_handler=on_error, before=[example_logging_task_decorator])
async def verify_payment_info(billing_information: Dict,
                              option_selected_id: str, order_id: str):
    success = bf.verify(billing_information)

    if not success:
        raise Exception("Could not verify billing information.")

    await client.publish_message("book_tickets", str(order_id))
    


@worker.task(task_type="book_tickets", exception_handler=on_error, before=[example_logging_task_decorator])
async def book_tickets():
    pass

def run_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.work())
