from typing import Dict

from pyzeebe import Job

from ticket_broker.use_cases.basic_use_cases import on_error
from ticket_broker.controlers.bank_adapter import BankAdapter
from ticket_broker.controlers.ticket_provider_adapter import TicketProviderAdapter
from ticket_broker.worker_instance import WorkerClientInstance


worker, client = WorkerClientInstance.get()

bank_verifier = BankAdapter()
journey_booker = TicketProviderAdapter()


@worker.task(task_type="verify_payment_info",
             exception_handler=on_error)
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
             exception_handler=on_error)
async def book_tickets(job: Job, billing_information: Dict,
                       selected_option: dict[str, str], order_id: str):
    """
    Books the tickets using the received billing details and the options.
    """

    success, tickets_details = journey_booker.book_journey(
        selected_option, billing_information)
    if success:
        await client.publish_message("confirm_order", str(order_id))
        return {"tickets_details": tickets_details}
    else:
        message = "Failed to book tickets"
        error_code = "booking_failed"
        await job.set_error_status(message, error_code)
