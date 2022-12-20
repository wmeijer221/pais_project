from ticket_broker.route_database import RouteDatabase

TEST_STATIONS = {
    "A": {
        "pretty_name": "Station A",
        "country": "AA"
    },
    "B": {
        "pretty_name": "Station B",
        "country": "BB"
    },
    "C": {
        "pretty_name": "Station C",
        "country": "CC"
    }
}

def test_route_database_creatable():
    assert RouteDatabase([], {}, {}) is not None
    assert RouteDatabase.from_file("data/railways.yaml") is not None

def test_load_notes():
    rdb = RouteDatabase([], TEST_STATIONS, {})
    assert "A" in rdb.graph
    assert "B" in rdb.graph
    assert "C" in rdb.graph
    assert "D" not in rdb.graph
