from ticket_broker.controlers.ticket_database import TicketDatabase
from ticket_broker.use_cases.basic_use_cases import on_error, logging_task_decorator
from ticket_broker.worker import worker

ticket_database = TicketDatabase()


@worker.task(task_type="load_ticket_details",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def load_ticket_details(order_id: str):
    """
    Loads ticket details from database and returns them.
    """

    journey_details = ticket_database.get_journey_details(order_id)
    formatted_details = []
    for index, detail in enumerate(journey_details):
        ticket = detail["ticket"]
        label = f'Ticket from {ticket["start_station"]} to {ticket["end_station"]} with {ticket["company"]}'
        formatted_details.append({"label": label, "value": index})
    return {"journey_details": formatted_details}


@worker.task(task_type="verify_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def verify_tickets(tickets_to_cancel: list, order_id: str):
    journey_details = ticket_database.get_journey_details(order_id)
    return {"tickets_are_valid": True}


@worker.task(task_type="cancel_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def cancel_tickets(tickets_to_cancel: list, order_id: str):
    ticket_database.remove_journey_legs(order_id, tickets_to_cancel)
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
