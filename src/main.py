"""
Implements basic camunda task.
"""

import time

from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult


# configuration for the Client
default_config = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


def handle_task(task: ExternalTask) -> TaskResult:
    """
    This task handler you need to implement with your business logic.
    After completion of business logic call either task.complete() or task.failure() or task.bpmn_error()
    to report status of task to Camunda
    """
    # add your business logic here
    # ...

    # mark task either complete/failure/bpmnError based on outcome of your business logic
    # this code simulate random failure
    failure, bpmn_error = random_true(), random_true()
    print(f'IM DOING THINGS: {failure=}, {bpmn_error=}')
    if failure:
        # this marks task as failed in Camunda
        return task.failure(error_message="task failed",  error_details="failed task details",
                            max_retries=3, retry_timeout=5000)
    elif bpmn_error:
        return task.bpmn_error(error_code="BPMN_ERROR_CODE", error_message="BPMN Error occurred",
                               variables={"var1": "value1", "success": False})

    # pass any output variables you may want to send to Camunda as dictionary to complete()
    return task.complete({"var1": 1, "var2": "value"})


def random_true():
    current_milli_time = int(round(time.time() * 1000))
    return current_milli_time % 2 == 0

if __name__ == '__main__':
    print("Starting external client.")
    ExternalTaskWorker(worker_id="1", config=default_config).subscribe(
        "topicName", handle_task)
