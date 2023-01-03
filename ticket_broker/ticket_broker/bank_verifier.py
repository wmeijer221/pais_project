
import random


class AbstractBankVerifier:
    """Abstract interface for bank verification logic."""

    def verify(self, iban: str) -> bool:
        """Stub for iban verification."""


class RandomChanceBankVerifier(AbstractBankVerifier):
    """Verifies banks based on random chance."""

    def __init__(self, failure_chance: float):
        self.failure_chance = failure_chance

    def verify(self, iban: str) -> bool:
        return random.random() > self.failure_chance


class BankVerifier:
    """Controller used to verify banking details."""

    _known_banks = {
        "ABNA": RandomChanceBankVerifier(0.0),
        "RABO": RandomChanceBankVerifier(0.0)
    }

    def verify(self, bank_details: dict) -> bool:
        """Verifies banking details with the relevant bank."""
        iban = bank_details["iban"]
        bank = self._identify_bank(iban)
        return bank.verify(iban)

    def _identify_bank(self, iban: str) -> AbstractBankVerifier:
        """Retrieves bank verifier strategy based on the provided IBAN."""
        bank_key = iban[4:8]
        return self._known_banks[bank_key]
