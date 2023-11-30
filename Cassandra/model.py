#!/usr/bin/env python3
import logging

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

#Definición de tabla para el modelo de aeropuertos
CREATE_PASSENGER_TRAFFIC_TABLE = """
    CREATE TABLE IF NOT EXISTS passenger_traffic (
        airline text,
        year int,
        month int,
        day int,
        from_location text,
        to_location text,
        age int,
        gender text,
        reason text,
        stay text,
        transit text,
        connection boolean,
        wait int,
        PRIMARY KEY ((airline, year), month)
    ) WITH CLUSTERING ORDER BY (month ASC);
    """
#Option 1 from the menu
def show_best_month_with_greater_influx_of_passengers(session, airline, year):
    year = int(year)
    query = session.prepare('SELECT month FROM passenger_traffic WHERE airline = ? AND year = ?;')
    rows = session.execute(query, [airline, year])

    # Contar pasajeros por mes
    passenger_counts = {}
    for row in rows:
        passenger_counts[row.month] = passenger_counts.get(row.month, 0) + 1

    # Encontrar el mes con el mayor número de pasajeros
    if passenger_counts:
        best_month = max(passenger_counts, key=passenger_counts.get)
        print(f"Best Month in {year} for {airline}: Month {best_month}")
    else:
        print("No data available for the given airline and year.")

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSENGER_TRAFFIC_TABLE)