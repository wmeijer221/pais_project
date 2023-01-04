
import logging
import os

from pyzeebe import ZeebeWorker, create_insecure_channel, ZeebeClient

from ticket_broker.singleton import Singleton

class WorkerInstance(Singleton):
    """Singleton class for the ZeebeWorker and Client"""

    def __new__(self):
        print("Creating ticket_broker worker")
        
        if "ENDPOINT_HOST" in os.environ.keys() and "ENDPOINT_PORT" in os.environ.keys():
            channel = create_insecure_channel(
                hostname=os.environ["ENDPOINT_HOST"], port=int(os.environ["ENDPOINT_PORT"]))
        else:
            logging.warning("No endpoint specified. Using defaults!")
            channel = create_insecure_channel()

        WorkerInstance._worker = ZeebeWorker(channel)
        WorkerInstance._client = ZeebeClient(channel)

    @classmethod
    def get(cls) -> tuple['ZeebeWorker', 'ZeebeClient']:
        return WorkerInstance._worker, WorkerInstance._client
