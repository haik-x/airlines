#!/usr/bin/env python3
import datetime
import random
import uuid
import csv

file_name = 'flight_passengers.csv'
#Lista donde se almacenarán los datos
data_list = []
#Abrir archivo CSV y leer datos
with open(file_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_list.append(row)

#Guardar los datos en un archivo de texto
with open('data.cql', 'w') as f:
    for item in data_list:
        print("INSERT INTO passenger_traffic(airline, from_location, to_location, day, month, year, age, gender, reason, stay, transit, connection, wait) VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}, '{7}', '{8}', '{9}', '{10}', {11}, {12});".format(
            item["airline"], item["from_location"], item["to_location"], int(item["day"]), int(item["month"]), int(item["year"]), int(item["age"]), item["gender"], item["reason"], item["stay"], item["transit"], str(item["connection"]).lower() == 'true', int(item["wait"])
        ), file=f)

CQL_FILE = 'data.cql'

def cql_stmt_generator():
    with open(CQL_FILE, 'w') as fd:
        for item in data_list:
            # Crear la consulta de inserción para cada fila en data_list
            query = (
                "INSERT INTO passenger_traffic(airline, from_location, to_location, day, month, year, age, gender, reason, stay, transit, connection, wait) "
                "VALUES ('{airline}', '{from_location}', '{to_location}', {day}, {month}, {year}, {age}, '{gender}', '{reason}', '{stay}', '{transit}', '{connection}', {wait});"
                .format(
                    airline = item["airline"],
                    from_location = item["from_location"],
                    to_location = item["to_location"],
                    day = int(item["day"]),
                    month = int(item["month"]),
                    year = int(item["year"]),
                    age = int(item["age"]),
                    gender = item["gender"],
                    reason = item["reason"],
                    stay = item["stay"],
                    transit = item["transit"],
                    connection = item["connection"],
                    wait = int(item["wait"])
                )
            )
            fd.write(query + "\n")


def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()