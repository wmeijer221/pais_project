import pytest

from ticket_broker.controlers.journey_booker import JourneyBooker

test_journey = {
    'order_id': 1672906979000,
    'selected_option': {
        'label': 'Journey from kobenhavn to stockholm consisting of: \nLeg from kobenhavn to malmo with sj\nLeg from malmo to goteborg with sj\nLeg from goteborg to stockholm with mtr_express\n',
        'value': [
            {
                'start_station': 'kobenhavn',
                'end_station': 'malmo',
                'traveltime_seconds': 4260,
                'price_eurocents_firstclass': 4212,
                'price_eurocents_economy': 2355,
                'company': 'sj'
            },
            {
                'start_station': 'malmo',
                'end_station': 'goteborg',
                'traveltime_seconds': 14510,
                'price_eurocents_firstclass': 7512,
                'price_eurocents_economy': 3655,
                'company': 'sj'
            },
            {
                'start_station': 'goteborg',
                'end_station': 'stockholm',
                'traveltime_seconds': 12780,
                'price_eurocents_firstclass': 5520,
                'price_eurocents_economy': 2340,
                'company': 'mtr_express'
            }
        ]
    },
    'billing_information': {
        'phone_number': '+31612345678',
        'email': 'john_doe@gmail.com',
        'full_name': 'John Doe',
        'national_id': '999999990X',
        'iban': 'NL02TRIO0123456789'
    }
}


def test_book_journey():
    jb = JourneyBooker()
    journey = test_journey["selected_option"]
    billing = test_journey['billing_information']
    success, tickets = jb.book_journey(journey, billing)
    assert success
    assert len(tickets) == len(journey["value"])
