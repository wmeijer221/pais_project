import json
import logging

from camunda.external_task.external_task import ExternalTask
from camunda.utils.log_utils import log_with_context

logging.root.setLevel(logging.WARNING)


def log(message, task: ExternalTask = None):
    """Log utility to log with context."""
    if task is None:
        log_context = {"WORKER_ID": -1, "TASK_ID": -1, "TOPIC": "n/a"}
    else:
        log_context = {"WORKER_ID": task.get_worker_id(),
                       "TASK_ID": task.get_task_id(),
                       "TOPIC": task.get_topic_name()}
    if isinstance(message, dict):
        message = json.dumps(message, indent=4)
    log_with_context(message, log_context, log_level='warning')
