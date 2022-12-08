"""
Implements very simple external task handler.
"""

import os


from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.client.engine_client import EngineClient

ENDPOINT_KEY = "ENDPOINT"
TOPIC_KEY = "TOPIC"


def task_handler(task: ExternalTask) -> TaskResult:
    return task.complete()


if __name__ == "__main__":
    ENDPOINT = os.getenv(ENDPOINT_KEY)
    BASE_URL = f'http://{ENDPOINT}/engine-rest'
    TOPIC_NAME = os.getenv(TOPIC_KEY)

    print(f'{BASE_URL=}\n{TOPIC_NAME=}')

    client = EngineClient(BASE_URL)
    worker = ExternalTaskWorker(worker_id=0, base_url=BASE_URL)
    worker.subscribe(TOPIC_NAME, task_handler)
