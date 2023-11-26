#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight

router = APIRouter()

@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(request: Request, flight: Flight = Body(...)):
    flight = jsonable_encoder(flight)
    new_flight = request.app.database["flight"].insert_one(flight)
    created_flight = request.app.database["flight"].find_one(
        {"_id": new_flight.inserted_id}
    )
    return created_flight

@router.get("/", response_description="Get all flights", response_model=List)
def list_flights(request: Request, airport:str):
    print(airport)
    if airport:
        group = [
            {"$match": {
                "to": airport, "connection": "False",
                "age":{"$gte": 18},
                "reason": {"$in":["On vacation/Pleasure", "Business/Work"]},
                "transit":{"$nin":["Own car"]}
                }
            },
            {
                "$group": {
                    "_id": "$month", 
                    "total_times": {"$sum": 1}
                }
            },
            {
                "$sort":{"total_times":-1}
            }
            ]
                              
    else:
        group = [
    {
        "$match": {
            "connection": "False",
            "age": {"$gte": 18},
            "reason": {"$in": ["On vacation/Pleasure", "Business/Work"]},
            "transit": {"$nin": ["Own car"]}
        }
    },
    {
        "$group": {
            "_id": {
                "to": "$to",
                "month": "$month"
            },
            "total_times": {"$sum": 1}
        }
    },
    {
        "$project": {
            "_id": 1,
            "total_times": 1,
            "to_lower": {"$toLower": "$_id.to"}
        }
    },
    {
        "$sort": {"to_lower": 1, "_id.month": 1}
    },
    {
        "$project": {
            "_id": 1,
            "total_times": 1
        }
    }
    ]

    pipeline = list(request.app.database["flights"].aggregate(group))
    return pipeline


