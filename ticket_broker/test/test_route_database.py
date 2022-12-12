def test_tables_importable():
    from ticket_broker.route_database import Station, Route, Company, conn
    assert Station is not None
    assert Route is not None
    assert Company is not None
    assert conn is not None
