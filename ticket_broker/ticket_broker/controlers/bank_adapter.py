"""
Implements template logic for bank interactions.
Giving a general idea of the interactions the application
is expected to have with banking systems.
"""

import random


class AbstractBank:
    """
    Abstract interface for bank adapter logic.
    """

    def verify_iban(self, iban: str) -> bool:
        """
        Stub for iban verification.
        """

    def pay(self, source_iban: str,
            target_iban: str,
            cost_in_eurocents: int) -> bool:
        """
        Stub for payment logic.
        """


class RandomChanceBank(AbstractBank):
    """
    Yields interaction successes based on random chance.
    """

    def __init__(self, verify_failure_chance: float,
                 payment_failure_chance: float):
        self.verify_failure_chance = verify_failure_chance
        self.payment_failure_chance = payment_failure_chance

    def verify_iban(self, iban: str) -> bool:
        return random.random() > self.verify_failure_chance

    def pay(self, source_iban: str, target_iban: str, cost_in_eurocents: int) -> bool:
        return random.random() > self.payment_failure_chance


class BankAdapter:
    """
    Facade that implements interaction logic with various banks.
    """

    _known_banks = {
        "TRIO": RandomChanceBank(0.0, 0.0),
        "RABO": RandomChanceBank(0.5, 0.5),
        "INGB": RandomChanceBank(1.0, 0.0),
        "ABNA": RandomChanceBank(0.0, 1.0),
    }

    def verify_bank_details(self, bank_details: dict) -> bool:
        """
        Verifies banking details with the relevant bank.
        """

        iban = bank_details["iban"]
        bank = self._get_bank_from_iban(iban)
        return bank.verify_iban(iban)

    def try_pay(self, cost_in_eurocents: int, source_bank_details: dict,
                target_bank_details: dict) -> bool:
        """
        Attempts to make payment between the two provided accounts.
        Returns success.
        """

        source_iban = source_bank_details["iban"]
        bank = self._get_bank_from_iban(source_iban)
        target_iban = target_bank_details["iban"]
        success = bank.pay(source_iban, target_iban, cost_in_eurocents)
        return success

    def _get_bank_from_iban(self, iban: str) -> AbstractBank:
        """
        Retrieves bank verifier strategy based on the provided IBAN.
        """

        bank_key = iban[4:8]
        return self._known_banks[bank_key]
