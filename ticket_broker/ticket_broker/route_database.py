import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship, Mapped

_ENGINE = db.create_engine("sqlite:///data/railways.sqlite3")
_METADATA = db.MetaData()

conn = _ENGINE.connect()
Base = declarative_base()


class Station(Base):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    slug = db.Column(db.Text)
    latitude = db.Column(db.REAL)
    longitude = db.Column(db.REAL)
    country = db.Column(db.Text)
    time_zone = db.Column(db.Text)
    is_city = db.Column(db.Text)
    is_main_station = db.Column(db.Text)
    is_airport = db.Column(db.Text)
    country_hint = db.Column(db.Text)
    same_as = db.Column(db.Integer)
    normalised_code = db.Column('normalised_code', db.Text)
    iata_airport_code = db.Column('iata_airport_code', db.Text)

    routes = relationship("Route", primaryjoin="or_(Route.start_station==Station.id,Route.end_station==Station.id )")


class Route(Base):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    start_station = db.Column(db.Integer, db.ForeignKey('stations.id'))
    end_station = db.Column(db.Integer, db.ForeignKey('stations.id'))

    traveltime_seconds = db.Column(db.Integer)
    price_eurocents_firstclass = db.Column(db.Integer)
    price_eurocents_economy = db.Column(db.Integer)
    company = db.Column(db.Integer, db.ForeignKey("company.id"))


class Company(Base):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    train_line_name = db.Column(db.Text)
