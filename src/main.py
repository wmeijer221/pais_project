"""
Implements very simple external task handler.
"""

import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.client.engine_client import EngineClient


ENDPOINT_KEY = "ENDPOINT"
TOPIC_KEY = "TOPIC"

logging.root.setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def __handle_task(task: ExternalTask) -> TaskResult:
    logger.critical("WIEHOO")
    vrs = task.get_variables()
    logger.critical(vrs)
    return task.complete()


def __create_worker(worker_id: int, worker_topic: str, base_url: str):
    worker = ExternalTaskWorker(worker_id=worker_id, base_url=base_url)
    worker.subscribe(worker_topic, __handle_task)


def __create_workers():
    ENDPOINT = os.getenv(ENDPOINT_KEY)
    BASE_URL = f'http://{ENDPOINT}/engine-rest'
    topic_names = str(os.getenv(TOPIC_KEY)).strip().split(";")

    logger.critical(f'{BASE_URL=}\n{topic_names=}')

    EngineClient(BASE_URL)
    executor = ThreadPoolExecutor(max_workers=len(topic_names))
    for index, topic in enumerate(topic_names):
        executor.submit(__create_worker, index, topic, BASE_URL)


if __name__ == "__main__":
    __create_workers()
