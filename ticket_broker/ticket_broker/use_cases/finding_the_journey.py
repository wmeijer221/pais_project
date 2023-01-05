from typing import Dict
from pathlib import Path

from ticket_broker.use_cases.base import logging_task_decorator
from ticket_broker.controlers.route_database import RouteDatabase
from ticket_broker.worker_instance import WorkerInstance


worker, client = WorkerInstance.get()

rdb = RouteDatabase.from_file(Path("data/railways.yaml"))


@worker.task(task_type="find_route_options", before=[logging_task_decorator])
async def find_route_options(journey_specification: Dict, order_id: str):
    """
    Finds route options and sends it to the customer.
    """

    if journey_specification['class'] == "first":
        weight = 'price_eurocents_firstclass'
    else:
        weight = 'price_eurocents_economy'

    options = rdb.find_route_options(journey_specification['start_station'],
                                     journey_specification['end_station'],
                                     weight)

    message = {"route_options": options}
    await client.publish_message("receive_journey_options", str(order_id), message)

    return message
