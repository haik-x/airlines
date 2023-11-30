#!/usr/bin/env python3
import logging
import os
import random

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('investments.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'investments')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: "Show best months with greater influx of passengers",
        2: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    while True:
            print_menu()
            option = int(input('Enter your choice: '))
            
            if option == 1:
                #Show best months with greater influx of passengers
                airline = input("Enter airline: ")
                year = int(input('Enter year: '))
                model.show_best_month_with_greater_influx_of_passengers(session, airline, year)
            elif option == 2:
                exit(0)

if __name__ == '__main__':
    main()
