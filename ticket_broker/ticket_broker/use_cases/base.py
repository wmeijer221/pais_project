import logging
from typing import Collection
from pyzeebe import Job

from ticket_broker.worker_instance import WorkerInstance

async def logging_task_decorator(job: Job) -> Job:
    """
    Logs the incoming job.
    """

    logging.info(f'\nReceived job {job.type} ({job.key})\n')
    return job


async def on_error(exception: Exception, job: Job):
    """
    Basic error handler.
    """

    status = f"Failed to handle job {job}. Error: {str(exception)}"
    logging.warning(status)
    await job.set_error_status(status)


worker, client = WorkerInstance.get()

@worker.task(task_type="select_option_from_key")
async def select_option_from_key(key: object, options: list[Collection]):
    """
    Forwards the details of the chosen option from the list of options.
    """

    return {"selected_option": options[key]}
