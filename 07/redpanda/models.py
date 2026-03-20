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
    lpep_pickup_datetime: str  # yyyy-MM-dd HH:mm:ss
    lpep_dropoff_datetime: str # yyyy-MM-dd HH:mm:ss
    
def ride_from_row(row):
    return Ride(
        PULocationID=int(row["PULocationID"]),
        DOLocationID=int(row["DOLocationID"]),
        trip_distance=float(row["trip_distance"]),
        tip_amount=float(row["tip_amount"]),
        passenger_count=int(row["passenger_count"]) if pd.notna(row["passenger_count"]) else None,
        total_amount=float(row["total_amount"]),
        lpep_pickup_datetime=row["lpep_pickup_datetime"].strftime('%Y-%m-%d %H:%M:%S'),
        lpep_dropoff_datetime=row["lpep_dropoff_datetime"].strftime('%Y-%m-%d %H:%M:%S')
    )

def ride_serializer(ride):
    ride_dict = asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')


def ride_deserializer(data):
    json_str = data.decode("utf-8")
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
