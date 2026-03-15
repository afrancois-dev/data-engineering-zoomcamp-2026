from typing import Optional
import json
import pandas as pd
from dataclasses import dataclass, asdict


@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    tip_amount: float
    passenger_count: Optional[int]
    total_amount: float
    lpep_pickup_datetime: int  # epoch milliseconds
    lpep_dropoff_datetime: int # epoch milliseconds
    
def ride_from_row(row):
    return Ride(
        PULocationID=int(row["PULocationID"]),
        DOLocationID=int(row["DOLocationID"]),
        trip_distance=float(row["trip_distance"]),
        tip_amount=float(row["tip_amount"]),
        passenger_count=int(row["passenger_count"]) if pd.notna(row["passenger_count"]) else None,
        total_amount=float(row["total_amount"]),
        lpep_pickup_datetime=int(row["lpep_pickup_datetime"].timestamp() * 1000),
        lpep_dropoff_datetime=int(row["lpep_dropoff_datetime"].timestamp() * 1000)
    )

def ride_serializer(ride):
    ride_dict = asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')


def ride_deserializer(data):
    json_str = data.decode("utf-8")
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
