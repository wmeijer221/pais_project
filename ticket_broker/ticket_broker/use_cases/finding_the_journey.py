from typing import Dict
from pathlib import Path

from ticket_broker.use_cases.basic_use_cases import on_error, logging_task_decorator
from ticket_broker.controlers.route_database import RouteDatabase
from ticket_broker.worker_instance import WorkerClientInstance


worker, client = WorkerClientInstance.get()

rdb = RouteDatabase.from_file(Path("data/railways.yaml"))

@worker.task(task_type="get_all_station_options",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def get_all_station_options(order_id: str):
    """
    Getter method for valid stations.
    """

    all_stations = rdb.get_all_stations()
    station_options = [{"label": station[1], "value": station[0]} 
                       for station in all_stations]
    return {"all_stations": station_options}

@worker.task(task_type="find_route_options",
             exception_handler=on_error,
             before=[logging_task_decorator])
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
