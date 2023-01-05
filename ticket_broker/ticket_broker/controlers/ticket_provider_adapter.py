"""
Implements template logic for ticket provider interactions.
Giving a general idea of the interactions the application
is expected to have with ticket providers.
"""

import random

from ticket_broker.controlers.bank_adapter import BankAdapter

system_banking_details = {"iban": "NL02TRIO0123456789"}


def rng(false_chance) -> bool:
    return random.random() > false_chance


_ticket_unavailable = 0.01
_nonrefundable_chance = 0.01


class TicketProvider:
    """
    Stub class for ticket provider adapters.
    """

    def book_ticket(self, ticket_details: dict) -> dict:
        trip_details = {
            "ticket": ticket_details,
            "billing": system_banking_details
        }
        return True, trip_details

    def get_ticket_details(self, ticket_details: dict) -> dict:
        details = ticket_details
        # TODO: Remove this once the price is set properly.
        details["price_eurocents"] = ticket_details["price_eurocents_economy"]
        return details

    def is_ticket_available(self, ticket_details: dict) -> bool:
        return rng(_ticket_unavailable)

    def cancel_tickets(self, ticket_details: dict) -> bool:
        return rng(_nonrefundable_chance)


class TicketProviderAdapter:
    """
    Generic adapter for interactions with various ticket booking platforms.
    """

    def __init__(self):
        self.bank_verifier = BankAdapter()

    def book_journey(self, journey: dict[str, str],
                     billing_information: dict) -> tuple[bool, list[dict]]:
        """
        Books entire journey.
        Returns tuple of success state and the acquired ticket details
        which is a ``list[dict]``: ``(success, details)``.
        If success is ``False``, the details are ``None``
        """

        leg_details = self._get_provider_per_lag(journey["value"])

        # check availability
        all_available = self._all_tickets_are_available(leg_details)
        if not all_available:
            return False, None

        ticket_details = self._get_ticket_details(leg_details)

        # check sufficient money.
        total_cost = sum([det["price_eurocents"] for det in ticket_details])
        success = self.bank_verifier.try_pay(total_cost, billing_information,
                                             system_banking_details)
        if not success:
            return False, None

        # Books tickets.
        success, ticket_details = self._book_all_tickets(leg_details)
        if not success:
            return False, None

        return True, ticket_details

    def _all_tickets_are_available(self, leg_details: list[dict, TicketProvider]) -> bool:
        availabilities = [provider.is_ticket_available(leg)
                          for leg, provider in leg_details]
        return all(availabilities)

    def _get_ticket_details(self, leg_details) -> list[dict]:
        return [provider.get_ticket_details(leg)
                for (leg, provider) in leg_details]

    def _get_provider_per_lag(self, trip) -> list[dict, TicketProvider]:
        return [(leg, self._get_provider_from_key(leg["company"]))
                for leg in trip]

    def _book_all_tickets(self, leg_details: list[dict, TicketProvider]) -> tuple[bool, list[dict]]:
        tickets = []
        for leg, provider in leg_details:
            success, details = provider.book_ticket(leg)
            if success:
                tickets.append(details)
            else:
                self.cancel_journey(tickets)
                return False, None
        return True, tickets

    def cancel_journey(self, trip_details: list[dict]):
        """
        Cancels a journey.
        """

        for leg in trip_details:
            provider_id = trip_details["ticket"]["ticket"]
            provider = self._get_provider_from_key(provider_id)
            provider.cancel_tickets(leg)

    def _get_provider_from_key(self, company_id: str) -> TicketProvider:
        """
        Retrieves bank verifier strategy based on the provided company ID.
        """

        return TicketProvider()
