
import random


class AbstractBankVerifier:
    """Abstract interface for bank verification logic."""

    def verify(self, iban: str) -> bool:
        """Stub for iban verification."""

    def pay(self, source_iban: str, target_iban: str, cost_in_eurocents: int) -> bool:
        """Stub for payment."""


class RandomChanceBankVerifier(AbstractBankVerifier):
    """Verifies banks based on random chance."""

    def __init__(self, verify_failure_chance: float, payment_failure_chance: float):
        self.verify_failure_chance = verify_failure_chance
        self.payment_failure_chance = payment_failure_chance

    def verify(self, iban: str) -> bool:
        return random.random() > self.verify_failure_chance

    def pay(self, source_iban: str, target_iban: str, cost_in_eurocents: int) -> bool:
        return random.random() > self.payment_failure_chance

class BankController:
    """Controller used to verify banking details."""

    _known_banks = {
        "TRIO": RandomChanceBankVerifier(0.0, 0.0),
        "RABO": RandomChanceBankVerifier(0.5, 0.5),
        "INGB": RandomChanceBankVerifier(1.0, 0.0),
        "ABNA": RandomChanceBankVerifier(0.0, 1.0),
    }

    def verify(self, bank_details: dict) -> bool:
        """Verifies banking details with the relevant bank."""
        iban = bank_details["iban"]
        bank = self._get_bank_from_iban(iban)
        return bank.verify(iban)

    def try_pay(self, cost_in_eurocents: int, source_bank_details: dict, 
                target_bank_details: dict) -> bool:
        source_iban = source_bank_details["iban"]
        bank = self._get_bank_from_iban(source_iban)
        target_iban = target_bank_details["iban"]
        success = bank.pay(source_iban, target_iban, cost_in_eurocents)
        return success

    def _get_bank_from_iban(self, iban: str) -> AbstractBankVerifier:
        """Retrieves bank verifier strategy based on the provided IBAN."""
        bank_key = iban[4:8]
        return self._known_banks[bank_key]
