import pytest

from ticket_broker.controlers.bank_verifier import BankController


def test_bank_verifier():
    verifier = BankController()
    details = {
        "iban": "NL02RABO0123456789"
    }
    success = verifier.verify(details)
    assert success

    fake_bank = "FAKE"
    details = {
        "iban": f"NL02{fake_bank}0123456789"
    }
    with pytest.raises(KeyError, match=f".*{fake_bank}.*"):
        verifier.verify(details)
