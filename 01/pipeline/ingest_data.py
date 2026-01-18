# coding: utf-8
#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import click


def load_table_to_db(engine: Engine, df: pd.DataFrame, table_name: str):
    df.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists="replace"
    )
    print(f"Table {table_name} created")
    
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append"
    )
    print(f"Table {table_name} loaded")

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
def ingest_data(user, password, host, port, db):
    year = 2025
    month = 11
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_green_trips = pd.read_parquet(f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet")
    df_zones = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')

    load_table_to_db(engine, df_green_trips, "green_trips")
    load_table_to_db(engine, df_zones, "zones")

if __name__ == "__main__":
    ingest_data()
