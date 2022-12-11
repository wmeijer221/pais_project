import time
import uuid
from camunda.client.engine_client import EngineClient

from log_util import log


def create_jobs(client: EngineClient):
    running = True
    PROCESS_KEY = "Process_05mjop3"
    while running:
        time.sleep(1)
        processes = client.get_process_instance()
        if len(processes) < 10:
            log("Creating new process")
            resp = client.start_process(process_key=PROCESS_KEY, variables={},
                                        business_key=str(uuid.uuid1()))
            log(resp)
