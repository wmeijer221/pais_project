from typing import Dict

from ticket_broker.use_cases.base import logging_task_decorator, on_error
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
async def verify_payment_info(billing_information: Dict):
    """
    Verifies the payment information of the consumer,
    making sure their account is valid..
    """

    success = bank_verifier.verify(billing_information)
    if not success:
        raise Exception("Could not verify billing information.")



@worker.task(task_type="book_tickets", exception_handler=on_error, before=[logging_task_decorator])
async def book_tickets(billing_information: Dict, selected_option: dict[str, str], order_id: str):
    """
    Books the tickets using the received billing details and the options.
    """

    success, tickets_details = journey_booker.book_journey(
        selected_option, billing_information)
    if success:
        await client.publish_message("confirm_order", str(order_id))
        return {"tickets_details": tickets_details}
    else:
        raise Exception("Could not order tickets.")
