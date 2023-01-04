import logging
import json
import random
import datetime

from ticket_broker.controlers.bank_verifier import BankController

def rng(false_chance) -> bool: 
    return random.random() > false_chance

_payment_failure_chance = 0.01
_ticket_unavailable = 0.01
_nonrefundable_chance = 0.01

class TicketProvider:
    def book_ticket(self, ticket_details: dict, payment_details: dict) -> dict:
        success = rng(_payment_failure_chance)
        if success:
            trip_details = {
                "ticket": ticket_details,
                "billing": payment_details
            }
            return True, trip_details
        else: 
            return False, None 

    def get_ticket_details(self, ticket_details: dict) -> dict:
        return ticket_details

    def is_ticket_available(self, ticket_details: dict) -> bool:
        return rng(_ticket_unavailable)

    def cancel_tickets(self, ticket_details: dict) -> bool:
        return rng(_nonrefundable_chance)
        

class JourneyBooker:
    def __init__(self):
        self.bank_verifier = BankController()

    def book_journey(self, journey: dict[str, str], billing_information: dict) -> tuple[bool, list[dict]]:
        leg_details = self._get_provider_per_lag(journey["value"])
        ticket_details = [provider.get_ticket_details(leg)
                          for (leg, provider) in leg_details]
        
        # check availability
        all_available = self._all_tickets_are_available(ticket_details)
        if not all_available:
            return False
        
        # check sufficient money.
        total_cost = sum([det["price_eurocents"] for det in ticket_details])
        system_banking_details = {"iban": "NL02TRIO0123456789"}
        success = self.bank_verifier.try_pay(total_cost, billing_information, 
                                             system_banking_details)
        if not success:
            return False
        
        # Books tickets.
        success, ticket_details = self._book_all_tickets(leg_details)
        if not success:
            return False

        return (True, ticket_details)

    def _all_tickets_are_available(self, leg_details: list) -> bool:
         return all([provider.is_ticket_available(leg)] 
                    for (leg, provider) in leg_details)

    def _get_provider_per_lag(self, trip) -> list[dict, TicketProvider]:
        return [(leg, self._get_provider_from_key(leg["company"])) for leg in trip]

    def _book_all_tickets(self, leg_details) -> tuple[bool, list[dict]]:
        tickets = []
        for leg, provider in leg_details:
            success, details = provider.book_ticket(leg)
            if success:
                tickets.append(details)
            else:
                self.cancel_journey(tickets)
                return False, None
        return (True, tickets)

    def cancel_journey(self, trip_details: list[dict]):
        for leg in trip_details:
            provider_id = trip_details["ticket"]["ticket"]
            provider= self._get_provider_from_key(provider_id)
            provider.cancel_tickets(leg)

    def _get_provider_from_key(self, company_id: str) -> TicketProvider:
        """Retrieves bank verifier strategy based on the provided company ID."""
        return TicketProvider()
