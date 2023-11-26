#!/usr/bin/env python3
import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")


def print_flights(flight):
    for k in flight.keys():
        print(f"{k}: {flight[k]}")
    print("-"*50)

def list_flight():
    print("Statistics for airports: ")
    option = input("Do you want statistics for a specific airport? (Y/N): ")
    if(option == "Y"):
        airport = input("Name of airport: ")
    else: 
        airport = ""
    suffix = "/flight"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "airport": airport,
    }
    
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flights(flight)
    else:
        print(f"Error: {response}")



def main():
    log.info(f"Welcome to our flight analizer. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")

    args = parser.parse_args()       

    if args.action == "search":
        list_flight()
    
    else:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

if __name__ == "__main__":
    main()