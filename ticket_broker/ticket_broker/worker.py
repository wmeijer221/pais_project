"""
Module for handling CAMUNDA tasks.
"""
import asyncio
import logging
import os

from pyzeebe import ZeebeWorker, ZeebeClient, create_insecure_channel

ENDPOINT_HOST_KEY = "ENDPOINT_HOST"
ENDPOINT_PORT_KEY = "ENDPOINT_PORT"


worker: ZeebeWorker = None
client: ZeebeClient = None

def create_client():
    global worker, client
    print("Creating worker/client instance")
    env_vars = os.environ.keys()
    if ENDPOINT_HOST_KEY in env_vars and ENDPOINT_PORT_KEY in env_vars:
        channel = create_insecure_channel(
            hostname=os.environ[ENDPOINT_HOST_KEY],
            port=int(os.environ[ENDPOINT_PORT_KEY]))
    else:
        logging.warning("No endpoint specified. Using defaults!")
        channel = create_insecure_channel()
    worker = ZeebeWorker(channel)
    client = ZeebeClient(channel)

def run_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.work())
