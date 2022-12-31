from pathlib import Path

from ticket_broker.route_database import RouteDatabase


def test_route_database_creatable():
    assert RouteDatabase([], {}, {}) is not None
    assert RouteDatabase.from_file(Path("data/test.yaml")) is not None


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
