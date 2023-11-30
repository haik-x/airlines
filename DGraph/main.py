#!/usr/bin/env python3
import os
import json  # Add this line

import pydgraph
from data.populateDGraph import *

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9081')

def print_menu():
    mm_options = {
        1: "Create data",
        2: "Airports and users with connections",
        3: "Airports and users with connections by specific city",
        4: "Drop All",
        5: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def read_json(file_path):
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()

def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    # Create schema
    set_schema(client)


    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            file_path = './data/flight_passengers.json'  # Replace with your actual file path
            data_list = read_json(file_path)
            create_data(client, data_list)
        if option == 2:
            analyze_connection(client,"")
        if option == 3:
            city = input("Write the name of the city you want to analyze: ")
            analyze_connection(client,city)
        if option == 4:
            drop_all(client)
        if option == 5:
            drop_all(client)
            close_client_stub(client_stub)
            exit(0)



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))
