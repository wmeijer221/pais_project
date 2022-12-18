from ticket_broker.route_database import RouteDatabase


def test_route_database_creatable():
    assert RouteDatabase([], {}, {}) is not None
    assert RouteDatabase.from_file("data/railways.yaml") is not None