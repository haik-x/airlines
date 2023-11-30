#!/usr/bin/env python3
import csv
import requests
from requests.exceptions import RequestException, HTTPError 

BASE_URL = "http://localhost:8000"

def main():
    with open("flight_passengers.csv") as fd:
        flights_csv = csv.DictReader(fd)
        for flight in flights_csv:
            del flight["id"]
            try:
                response = requests.post(BASE_URL+"/flight", json=flight)
                response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            except HTTPError as e:  # Use HTTPError directly
                print(f"Failed to post flight {flight}. Error: {e}")
                print(f"Response content: {response.text}")
            except RequestException as e:
                print(f"Request error: {e}")

if __name__ == "__main__":
    main()