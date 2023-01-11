from pathlib import Path

from ticket_broker.controlers.route_database import RouteDatabase


def test_route_database_creatable():
    assert RouteDatabase([], {}, {}) is not None
    assert RouteDatabase.from_file(Path("data/test.yaml")) is not None

def test_get_all_stations():
    rdb = RouteDatabase.from_file(Path("data/test.yaml"))
    station_count = 3
    stations = rdb.get_all_stations()
    assert len(stations) == station_count
    assert all([isinstance(station, tuple) for station in stations])
    station_keys = ["a", "b", "c"]
    pretty_names = ["Test station A", "Test station B", "Test station C"]
    for entry, exp_key, exp_name in zip(stations, station_keys, pretty_names):
        assert isinstance(exp_name[0], str)
        assert isinstance(exp_name[1], str)
        assert exp_key == entry[0]
        assert exp_name == entry[1]

def test_load_data():
    """
    Tests if the contents of the railway data file gets loaded correctly.
    """
    rdb = RouteDatabase.from_file(Path("data/test.yaml"))
    assert "a" in rdb.graph
    assert "b" in rdb.graph
    assert "c" in rdb.graph
    assert "d" not in rdb.graph

    assert ["a", "b"] in rdb.graph.edges
    assert ["b", "c"] in rdb.graph.edges
    assert ["a", "c"] not in rdb.graph.edges

    assert "corp_a" in rdb.companies.keys()
    assert "corp_b" in rdb.companies.keys()
    assert "local" in rdb.companies.keys()


def test_find_route():
    """
    Tests if the pathfinder finds the right routs.
    """
    rdb = RouteDatabase.from_file(Path("data/test.yaml"))

    route_a_c_fastest = rdb.find_route_options("a", "c", "traveltime_seconds")[0]
    route_a_c_cheapest = rdb.find_route_options("a", "c", "price_eurocents_economy")[0]

    # Test that the algorithm prioritises the right thing
    assert len(route_a_c_fastest["value"]) == 2
    assert route_a_c_fastest["value"][0]["company"] == "corp_a"

    assert len(route_a_c_cheapest["value"]) == 2
    assert route_a_c_cheapest["value"][0]["company"] == "corp_b"
