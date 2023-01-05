import pytest

from ticket_broker.controlers.bank_adapter import BankAdapter


def test_bank_verifier():
    verifier = BankAdapter()
    details = {
        "iban": "NL02TRIO0123456789"
    }
    success = verifier.verify_bank_details(details)
    assert success

    fake_bank = "FAKE"
    details = {
        "iban": f"NL02{fake_bank}0123456789"
    }
    with pytest.raises(KeyError, match=f".*{fake_bank}.*"):
        verifier.verify_bank_details(details)
