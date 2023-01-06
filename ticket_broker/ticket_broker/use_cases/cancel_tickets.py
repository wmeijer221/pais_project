from typing import Dict

from ticket_broker.use_cases.basic_use_cases import on_error, logging_task_decorator
from ticket_broker.worker_instance import WorkerClientInstance


worker, client = WorkerClientInstance.get()


@worker.task(task_type="verify_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def verify_tickets(tickets_to_cancel: Dict, order_id: str):
    return {"tickets_are_valid": True}


@worker.task(task_type="cancel_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def cancel_tickets(tickets_to_cancel: Dict, order_id: str):
    return {
        "successfully_canceled_tickets": tickets_to_cancel,
        "unsuccessfully_canceled_tickets": [],
        "canceled_tickets_price": 0
    }


@worker.task(task_type="refund_money",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def refund_money(order_id: str, canceled_tickets_price: int):
    pass


@worker.task(task_type="load_ticket_details",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def load_ticket_details(order_id: str):
    journey = {
        "journey_details": [
            {"label": "leg 1", "value": "asdf"},
            {"label": "leg 2", "value": "some_id"},
            {"label": "leg 3", "value": "some_other_id"}
        ]
    }
    return journey
