"""Diner database with plain SQL."""

import sqlite3

connection: sqlite3.Connection


def open_connection():
    """
    Open a connection to the SQLite database file "diners_plain.db" and set the global variable 'connection'
    to the Connection object.
    """
    global connection
    connection = sqlite3.connect("diners_plain.db")


def close_connection():
    """Close the database connection."""
    connection.close()


def create_tables():
    """Create the 'provider' and 'canteen' tables in the database using SQL queries."""
    # SQL query for creating the 'provider' table.
    create_provider = """
        CREATE TABLE provider (
        id INTEGER PRIMARY KEY,
        provider_name VARCHAR
        );
        """

    # SQL query for creating the 'canteen table'
    create_canteen = """
        CREATE TABLE canteen (
        id INTEGER PRIMARY KEY NOT NULL,
        provider_id INTEGER,
        name VARCHAR,
        location VARCHAR,
        time_open VARCHAR(5),
        time_closed VARCHAR(5),
        FOREIGN KEY (provider_id) REFERENCES provider(id)
        );
        """

    connection.execute(create_provider)
    connection.execute(create_canteen)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.commit()


def delete_tables():
    """Delete the 'canteen' and 'provider' tables from the database."""
    connection.execute("DROP TABLE canteen")
    connection.execute("DROP TABLE provider")
    connection.commit()


def create_records():
    """Insert predefined records into the 'provider' and 'canteen' tables in the database using SQL queries."""
    # The provider of bitStop kohvik, adds it to the database
    connection.execute("""
        INSERT INTO provider (provider_name)
        VALUES ("Bitt OÜ")
        """)

    # Canteen in IT College, its provider's id, location and open time, adds it to the database
    connection.execute("""
        INSERT INTO canteen (name, provider_id, location, time_open, time_closed)
        VALUES ("bitStop KOHVIK", 1, "IT College, Raja 4c", "09:30", "16:00")
        """)

    # Providers of the canteens in TalTech
    providers = [
        ("Rahva Toit",),
        ("Baltic Restaurants Estonia AS",),
        ("TTÜ Sport OÜ",)
    ]

    # List of canteens in TalTech, their provider's id, location and open times
    canteens = [
        ("Economics- and social science building canteen", 2, "Akadeemia tee 3\nSOC- building", "08:30", "18:30"),
        ("Library canteen", 2, "Akadeemia tee 1/Ehitajate tee 7", "08:30", "19:00"),
        ("Main building Deli cafe", 3, "Ehitajate tee 5\nU01 building", "09:00", "16:30"),
        ("Main building Daily lunch restaurant", 3, "Ehitajate tee 5\nU01 building", "09:00", "16:30"),
        ("U06 building canteen", 2, None, "09:00", "16:00"),
        ("Natural Science building canteen", 3, "Akadeemia tee 15\nSCI building", "09:00", "16:00"),
        ("ICT building canteen", 3, "Raja 15/Mäepealse 1", "09:00", "16:00"),
        ("Sports building canteen", 4, "Männiliiva 7\nS01 building", "11:00", "20:00")
    ]

    # Adds the providers to the database
    connection.executemany(
        """
        INSERT INTO provider (provider_name)
        VALUES (?)
        """,
        providers
    )

    # Adds the canteens to the database
    connection.executemany(
        """
        INSERT INTO canteen (name, provider_id, location, time_open, time_closed)
        VALUES (?, ?, ?, ?, ?)
        """,
        canteens
    )

    connection.commit()


def find_canteens_by_open_time() -> list:
    """
    Retrieve the names of canteens from the 'canteen' table in the database that are open from 09:00 to 16:20,
    and return the results as a list.
    """
    cursor = connection.execute(
        """
        SELECT name 
        FROM canteen
        WHERE time_open <= "09:00"
        AND time_closed >= "16:20"
        """
    )

    return [i[0] for i in cursor]


def find_canteens_by_provider() -> list:
    """
    Retrieve the names of canteens from the 'canteen' table in the database that are
    provided by Baltic Restaurants Estonia AS and return the results as a list.
    """
    cursor = connection.execute(
        """
        SELECT c.name
        FROM canteen c
        JOIN provider p ON p.id = c.provider_id
        WHERE p.provider_name = "Baltic Restaurants Estonia AS";
        """
    )

    return [i[0] for i in cursor]


if __name__ == '__main__':
    open_connection()
    delete_tables()
    create_tables()
    create_records()
    print(find_canteens_by_open_time())
    print(find_canteens_by_provider())
    close_connection()
