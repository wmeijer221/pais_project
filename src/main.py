"""
Implements very simple external task handler.
"""

import logging
import os
import random
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.client.engine_client import EngineClient
from camunda.utils.log_utils import log_with_context


ENDPOINT_KEY = "ENDPOINT"
TOPIC_KEY = "TOPIC"

logging.root.setLevel(logging.WARNING)


def log(message: str, task: ExternalTask = None):
    """Log utility to log with context."""
    if task is None:
        log_context = {"WORKER_ID": -1, "TASK_ID": -1, "TOPIC": "no_topic"}
    else:
        log_context = {"WORKER_ID": task.get_worker_id(),
                       "TASK_ID": task.get_task_id(),
                       "TOPIC": task.get_topic_name()}
    log_with_context(message, log_context, log_level='warning')


def __handle_task(task: ExternalTask) -> TaskResult:
    """Handles an external task."""
    vrs = task.get_variables()
    log(vrs, task)
    if random.random() > 0.5:
        log("completing!", task)
        return task.complete()
    else:
        log("failing!", task)
        return task.failure("Random fault...", error_details="something something", max_retries=10, retry_timeout=5)


def __create_worker(worker_id: int, worker_topic: str, base_url: str):
    """Creates a single worker for a single topic."""
    worker = ExternalTaskWorker(worker_id=worker_id, base_url=base_url)
    worker.subscribe(worker_topic, __handle_task)


def __create_workers():
    """Creates external workers for each topic."""
    # Loads relevant parameters from environment variables.
    endpoint = os.getenv(ENDPOINT_KEY)
    endpoint = f'http://{endpoint}/engine-rest'
    topics = str(os.getenv(TOPIC_KEY)).strip().split(";")

    log({"endpoint": endpoint, "topics": topics})

    # Creates external worker clients for each of the topics.
    EngineClient(endpoint)
    executor = ThreadPoolExecutor(max_workers=len(topics))
    for index, topic in enumerate(topics):
        executor.submit(__create_worker, index, topic, endpoint)


if __name__ == "__main__":
    __create_workers()
