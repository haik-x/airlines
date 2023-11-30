#!/usr/bin/env python3
import os

from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as flight_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'project')

app = FastAPI()

def create_indexes():
    mongodb_client = MongoClient(MONGODB_URI)
    database = mongodb_client[DB_NAME]
    flights_collection = database["flights"]

    flights_collection.create_index([
        ("to", 1),
        ("connection", 1),
        ("age", 1),
        ("reason", 1),
        ("transit", 1),
        ("month", 1),
    ])

    flights_collection.create_index([
        ("connection", 1),
        ("age", 1),
        ("reason", 1),
        ("transit", 1),
        ("to", 1),
        ("month", 1),
    ])

    mongodb_client.close()

@app.on_event("startup")
def startup_db_client():
    create_indexes()
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")

app.include_router(flight_router, tags=["flight"], prefix="/flight")