import logging

class JourneyBooker:
    def book_journey(self, journey: dict[str, str], billing_information: dict):
        for step in journey:
            logging.debug(step)
    