from pyzeebe import Job
import requests
from typing import Dict

from ticket_broker.use_cases.basic_use_cases import on_error, logging_task_decorator
from ticket_broker.controlers.bank_adapter import BankAdapter
from ticket_broker.controlers.ticket_database import TicketDatabase
from ticket_broker.controlers.ticket_provider_adapter import TicketProviderAdapter
from ticket_broker.worker import worker, client

bank_verifier = BankAdapter()
journey_booker = TicketProviderAdapter()
ticket_database = TicketDatabase()


@worker.task(task_type="verify_payment_info",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def verify_payment_info(job: Job, billing_information: Dict):
    """
    Verifies the payment information of the consumer,
    making sure their account is valid..
    """

    success = bank_verifier.verify_bank_details(billing_information)
    if success:
        return {"billing_is_verified": success}
    else:
        message = "Failed to verify payment information."
        error_code = "verification_failed"
        await job.set_error_status(message, error_code)


@worker.task(task_type="book_tickets",
             exception_handler=on_error,
             before=[logging_task_decorator])
async def book_tickets(job: Job, billing_information: Dict,
                       selected_option: dict[str, str], order_id: str):
    """
    Books the tickets using the received billing details and the options.
    """

    success, tickets_details = journey_booker.book_journey(
        selected_option, billing_information)
    if success:
        ticket_database.store_new_journey(str(order_id), tickets_details)
        send_tickets_to_content_server(tickets_details, order_id)
        await client.publish_message("confirm_order", str(order_id))
        return {"tickets_details": tickets_details}
    else:
        message = "Failed to book tickets"
        error_code = "booking_failed"
        await job.set_error_status(message, error_code)


def send_tickets_to_content_server(tickets: list[dict], order_id: str):
    json_message = {
        "order_id": order_id,
        "tickets": tickets,
    }
    url = "http://content_api:8000/set_latest_ticket"
    requests.post(url, json=json_message, verify=False)
