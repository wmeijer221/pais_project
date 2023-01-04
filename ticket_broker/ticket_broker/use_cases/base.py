import logging

from pyzeebe import Job


async def logging_task_decorator(job: Job) -> Job:
    logging.debug(f'\nReceived job {job.type} ({job.key})\n')
    return job

async def on_error(exception: Exception, job: Job):
    """Basic error handler."""
    status = f"Failed to handle job {job}. Error: {str(exception)}"
    logging.warning(status)
    await job.set_error_status(status)
