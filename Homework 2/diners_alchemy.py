"""Diner database with SQLAlchemy."""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///diners_alchemy.db")
Session = sessionmaker(bind=engine)
session: Session = Session()


class Provider(Base):
    """Class representing the 'provider' table in the 'diners_alchemy' database."""
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True)
    provider_name = Column(String)


class Canteen(Base):
    """Class representing the 'canteen' table in the 'diners_alchemy' database."""
    __tablename__ = "canteen"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("provider.id"))
    name = Column(String)
    location = Column(String)
    time_open = Column(String(5))
    time_closed = Column(String(5))
    provider = relationship(Provider)


def create_tables():
    """Create database tables based on the defined ORM classes."""
    Base.metadata.create_all(engine)


def delete_tables():
    """Delete all existing database tables."""
    Base.metadata.drop_all(engine)


def create_records():
    """Insert predefined records into the 'provider' and 'canteen' tables in the database using SQLAlchemy commands."""
    # The provider of bitStop kohvik, adds it to the database
    session.add(Provider(provider_name="Bitt OÜ"))

    # Canteen in IT College, its provider's id, location and open time, adds it to the database
    session.add(Canteen(name="bitStop KOHVIK", provider_id=1, location="IT College, Raja 4c",
                        time_open="09:30", time_closed="16:00"))

    # Providers of the canteens in TalTech
    providers = [
        Provider(provider_name="Rahva Toit"),
        Provider(provider_name="Baltic Restaurants Estonia AS"),
        Provider(provider_name="TTÜ Sport OÜ")
    ]
    session.add_all(providers)

    # List of canteens in TalTech, their provider's id, location and open times
    canteens = [
        Canteen(name="Economics- and social science building canteen", provider_id=2,
                location="Akadeemia tee 3\nSOC- building", time_open="08:30", time_closed="18:30"),
        Canteen(name="Library canteen", provider_id=2, location="Akadeemia tee 1/Ehitajate tee 7",
                time_open="08:30", time_closed="19:00"),
        Canteen(name="Main building Deli cafe", provider_id=3, location="Ehitajate tee 5\nU01 building",
                time_open="09:00", time_closed="16:30"),
        Canteen(name="Main building Daily lunch restaurant", provider_id=3, location="Ehitajate tee 5\nU01 building",
                time_open="09:00", time_closed="16:30"),
        Canteen(name="U06 building canteen", provider_id=2, time_open="09:00", time_closed="16:00"),
        Canteen(name="Natural Science building canteen", provider_id=3, location="Akadeemia tee 15\nSCI building",
                time_open="09:00", time_closed="16:00"),
        Canteen(name="ICT building canteen", provider_id=3, location="Raja 15/Mäepealse 1",
                time_open="09:00", time_closed="16:00"),
        Canteen(name="Sports building canteen", provider_id=4, location="Männiliiva 7\nS01 building",
                time_open="11:00", time_closed="20:00")
    ]
    session.add_all(canteens)
    session.commit()


def find_canteens_by_open_time() -> list:
    """
    Retrieve the names of canteens from the 'canteen' table in the database that are open from 09:00 to 16:20,
    and return the results as a list.
    """
    canteens = session.query(Canteen).filter(Canteen.time_open <= "09:00", Canteen.time_closed >= "16:20").all()
    return [canteen.name for canteen in canteens]


def find_canteens_by_provider() -> list:
    """
    Retrieve the names of canteens from the 'canteen' table in the database that are
    provided by Baltic Restaurants Estonia AS and return the results as a list.
    """
    canteens = session.query(Canteen).join(Provider).filter(
        Provider.provider_name == "Baltic Restaurants Estonia AS"
    ).all()
    return [canteen.name for canteen in canteens]


if __name__ == '__main__':
    delete_tables()
    create_tables()
    create_records()
    print(find_canteens_by_open_time())
    print(find_canteens_by_provider())

session.close()
