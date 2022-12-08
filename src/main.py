
from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.client.engine_client import EngineClient


def task_handler(task: ExternalTask) -> TaskResult:
    return task.complete()


if __name__ == "__main__":
    # TODO: replace with environment variable.
    BASE_URL = "http://cam-workflow:8080/engine-rest"
    TOPIC_NAME = "topicName"

    client = EngineClient(BASE_URL)
    worker = ExternalTaskWorker(worker_id=0, base_url=BASE_URL)
    worker.subscribe(TOPIC_NAME, task_handler)
    