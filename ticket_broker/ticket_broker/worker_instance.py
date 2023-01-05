import logging
import os

from pyzeebe import ZeebeWorker, ZeebeClient, create_insecure_channel

from ticket_broker.singleton import Singleton

ENDPOINT_HOST_KEY = "ENDPOINT_HOST"
ENDPOINT_PORT_KEY = "ENDPOINT_PORT"


class WorkerClientInstance(Singleton):
    """
    Singleton class for the ZeebeWorker and ZeebeClient
    """

    def __new__(cls, *args, **kwargs):
        print("Creating worker/client instance")
        env_vars = os.environ.keys()
        if ENDPOINT_HOST_KEY in env_vars and ENDPOINT_PORT_KEY in env_vars:
            channel = create_insecure_channel(
                hostname=os.environ[ENDPOINT_HOST_KEY],
                port=int(os.environ[ENDPOINT_PORT_KEY]))
        else:
            logging.warning("No endpoint specified. Using defaults!")
            channel = create_insecure_channel()
        WorkerClientInstance._worker = ZeebeWorker(channel)
        WorkerClientInstance._client = ZeebeClient(channel)

    @classmethod
    def get(cls) -> tuple['ZeebeWorker', 'ZeebeClient']:
        """
        Returns the ZeebeWorker and ZeebeClient instances.
        """

        return WorkerClientInstance._worker, WorkerClientInstance._client
