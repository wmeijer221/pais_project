import logging
from typing import Collection, Dict
from pyzeebe import Job

from ticket_broker.worker import worker, client, logger
from ticket_broker._version import NAME


async def logging_task_decorator(job: Job) -> Job:
    """
    Logs the incoming job.
    """

    logger.info(f'Received job {job.type} ({job.key})')
    return job


async def on_error(exception: Exception, job: Job):
    """
    Basic error handler.
    """

    status = f"Failed to handle job {job}. Error: {str(exception)}"
    logger.warning(status)
    await job.set_error_status(status)


@worker.task(task_type="select_option_from_key",
             before=[logging_task_decorator])
async def select_option_from_key(job: Job, key: object, options: list[Collection]):
    """
    Forwards the details of the chosen option from the list of options.
    """

    try:
        return {"selected_option": options[key]}
    except LookupError as exception:
        message = str(exception)
        error_code = "selection_option_from_key_error"
        await job.set_error_status(message, error_code)


@worker.task(task_type="send_message_forward_data",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def send_message_forward_data(name: str, correlation_key: str, variables: Dict):
    """
    Forwards data sent in this message to the provided target.
    """

    await client.publish_message(
        name=name,
        correlation_key=str(correlation_key),
        variables=variables)


@worker.task(task_type="send_message",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def send_message(name: str, correlation_key: str):
    """
    Forwards message to the provided target.
    """

    await client.publish_message(
        name=name,
        correlation_key=str(correlation_key))
