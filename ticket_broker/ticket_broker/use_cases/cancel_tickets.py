from typing import Dict

from ticket_broker.use_cases.basic_use_cases import on_error, logging_task_decorator
from ticket_broker.worker_instance import WorkerClientInstance


worker, client = WorkerClientInstance.get()


@worker.task(task_type="verify_payment_info",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def verify_tickets(canceled_tickets: Dict, order_id: str):
    tickets = canceled_tickets["tickets"]
    return {"tickets_are_valid": True}


@worker.task(task_type="cancel_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def cancel_tickets(canceled_tickets: Dict, order_id: str):
    tickets = canceled_tickets["tickets"]
    return {
        "successfully_canceled_tickets": tickets,
        "unsuccessfully_canceled_tickets": [],
        "canceled_tickets_price": 0
    }


@worker.task(task_type="refund_money",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def refund_money(order_id: str, canceled_tickets_price: int):
    pass
