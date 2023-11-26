#!/usr/bin/env python

"""
Generador de datos para proyecto de Bases de Datos No Relacionales
ITESO 
"""
import argparse
import json
import random
import datetime

from random import choice, randint, randrange


airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date


def generate_dataset(output_file, rows):
    data = []
    for i in range(rows):
        from_airport = random.choice(airports)
        to_airport = random.choice(airports)
        while from_airport == to_airport:
            to_airport = random.choice(airports)
        date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
        reason = random.choice(reasons)
        stay = random.choice(stays)
        connection = random.choice(connections)
        wait = random.randint(30, 720)
        transit = random.choice(transits)

        if not connection:
           wait = 0
        else:
            transit = ""

        if reason == "Back Home":
            stay = "Home"
            connection = False
            wait = 0
            transit = random.choice(transits)

        line = {
            "airline": random.choice(airlines),
            "from": from_airport,
            "to": to_airport,
            "day": date.day,
            "month": date.month,
            "year": date.year,
            "age": random.randint(1, 90),
            "gender": random.choice(genders),
            "reason": reason,
            "stay": stay,
            "transit": transit,
            "connection": connection,
            "wait": wait,
        }
        data.append(line)

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

generate_dataset('flight_passengers.json', 1000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output",
            help="Specify the output filename of your csv, defaults to: flight_passengers.json", default="flight_passengers.json")
    parser.add_argument("-r", "--rows",
            help="Amount of random generated entries for the dataset, defaults to: 1000", type=int, default=1000)

    args = parser.parse_args()
    
    print(f"Generating {args.rows} for flight passenger dataset")
    generate_dataset(args.output, args.rows)
    print(f"Completed generating dataset in {args.output}")


