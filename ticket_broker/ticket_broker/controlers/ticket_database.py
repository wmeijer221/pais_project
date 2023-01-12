"""
Stub class for real database interactions.
Giving an idea of the different interactions with real databases.
"""

from typing import Dict


class TicketDatabase:
    """
    Database class for ticket management.
    """

    journeys: Dict = {}
    tickets: Dict = {}

    def store_new_journey(self, order_id: str, ticket_details: Dict):
        """
        Stores a new journey in the database.
        """

        self.journeys[order_id] = ticket_details
        

    def get_journey_details(self, order_id) -> Dict:
        """
        Retrieves journey details form the database.
        Returns ``None`` if it does not exist.
        """

        if order_id in self.journeys:
            return self.journeys[order_id]
        else:
            return None

    def journey_exists(self, order_id: str) -> bool:
        """
        Checks if there exists a journey with the given ``order_id``.
        Return ``True`` if there is.
        """

        return order_id in self.journeys
