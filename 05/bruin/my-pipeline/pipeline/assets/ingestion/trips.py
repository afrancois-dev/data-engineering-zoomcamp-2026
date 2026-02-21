"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: When the meter was engaged
  - name: dropoff_datetime
    type: timestamp
    description: When the meter was disengaged
  - name: pickup_location_id
    type: integer
    description: Where the trip started
  - name: dropoff_location_id
    type: integer
    description: Where the trip ended
  - name: fare_amount
    type: double
    description: The fare amount
  - name: taxi_type
    type: string
    description: The type of taxi (yellow, green)
  - name: payment_type
    type: integer
    description: The payment type id

@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def materialize():
    # Bruin provides these environment variables for the date range to be processed
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    
    # Parse dates to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Get taxi types from BRUIN_VARS, default to ["yellow", "green"] if not provided
    vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = vars.get("taxi_types", ["yellow", "green"])

    all_dfs = []
    
    # Iterate through each month in the range
    current_dt = start_dt.replace(day=1)
    while current_dt <= end_dt:
        year = current_dt.year
        month = f"{current_dt.month:02}"
        
        for taxi_type in taxi_types:
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month}.parquet"
            print(f"Fetching data from {url}...")
            try:
                # Read the parquet file directly from the URL
                df = pd.read_parquet(url)
                
                # Standardize column names
                rename_map = {
                    "tpep_pickup_datetime": "pickup_datetime",
                    "tpep_dropoff_datetime": "dropoff_datetime",
                    "lpep_pickup_datetime": "pickup_datetime",
                    "lpep_dropoff_datetime": "dropoff_datetime",
                    "PULocationID": "pickup_location_id",
                    "DOLocationID": "dropoff_location_id",
                    "fare_amount": "fare_amount",
                    "payment_type": "payment_type"
                }
                df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
                
                # Add taxi_type column
                df["taxi_type"] = taxi_type

                # Filter rows to only include those within the requested date range
                mask = (df['pickup_datetime'] >= pd.Timestamp(start_dt)) &                        (df['pickup_datetime'] <= pd.Timestamp(end_dt).replace(hour=23, minute=59, second=59))
                df = df.loc[mask]
                
                if not df.empty:
                    # Only keep columns defined in the asset metadata
                    required_columns = ["pickup_datetime", "dropoff_datetime", "pickup_location_id", "dropoff_location_id", "fare_amount", "taxi_type", "payment_type"]
                    # Ensure all required columns exist (even if with NA)
                    for col in required_columns:
                        if col not in df.columns:
                            df[col] = None
                    
                    df = df[required_columns]
                    all_dfs.append(df)
                    
            except Exception as e:
                print(f"Failed to fetch or process {url}: {e}")
        
        # Move to the next month
        current_dt += relativedelta(months=1)

    if not all_dfs:
        # Return an empty dataframe with correct columns if no data was found
        return pd.DataFrame(columns=["pickup_datetime", "dropoff_datetime", "pickup_location_id", "dropoff_location_id", "fare_amount", "taxi_type", "payment_type"])
        
    return pd.concat(all_dfs, ignore_index=True)
