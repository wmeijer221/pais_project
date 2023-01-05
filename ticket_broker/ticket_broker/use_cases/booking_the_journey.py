from typing import Dict

from pyzeebe import Job

from ticket_broker.use_cases.base import on_error
from ticket_broker.controlers.bank_verifier import BankController
from ticket_broker.controlers.journey_booker import JourneyBooker
from ticket_broker.worker_instance import WorkerInstance


worker, client = WorkerInstance.get()

bank_verifier = BankController()
journey_booker = JourneyBooker()


@worker.task(task_type="send_order_placement")
async def send_order_placement(billing_information: Dict, option_selected_id: str, order_id: str):
    """
    Message exchange logic for moving a message from the consumer to the broker.
    """

    # TODO: This is boilerplate code; is there a way to remove this?
    message = {
        "billing_information": billing_information,
        "option_selected_id": option_selected_id
    }
    await client.publish_message("wait_for_order", str(order_id), message)


@worker.task(task_type="verify_payment_info", exception_handler=on_error)
async def verify_payment_info(job: Job, billing_information: Dict):
    """
    Verifies the payment information of the consumer,
    making sure their account is valid..
    """

    success = bank_verifier.verify(billing_information)
    if success:
        return { "billing_is_verified": success }
    else:
        message = "Failed to verify payment information."
        error_code = "verification_failed"
        await job.set_error_status(message, error_code)


@worker.task(task_type="book_tickets", exception_handler=on_error)
async def book_tickets(job: Job, billing_information: Dict, selected_option: dict[str, str], order_id: str):
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
