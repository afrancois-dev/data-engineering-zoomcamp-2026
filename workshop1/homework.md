
# DLT


## Beforehand (set-up)
```
(taxi-pipelines) @afrancois-dev ➜ /workspaces/data-engineering-zoomcamp-2026/workshop1/taxi-pipelines (main) $ python taxi_pipeline.py
2026-03-02 18:09:30,306|[WARNING]|21949|138484746282816|dlt|validate.py|verify_normalized_table:91|In schema `taxi_pipeline_source`: The following columns in table 'taxi_data' did not receive any data during this load and therefore could not have their types inferred:
  - rate_code
  - mta_tax

Unless type hints are provided, these columns will not be materialized in the destination.
One way to provide type hints is to use the 'columns' argument in the '@dlt.resource' decorator.  For example:

@dlt.resource(columns={'rate_code': {'data_type': 'text'}})

Pipeline taxi_pipeline load step completed in 1.59 seconds
1 load package(s) were loaded to destination duckdb and into dataset nyc_taxi_data
The duckdb destination used duckdb:////workspaces/data-engineering-zoomcamp-2026/taxi_pipeline.duckdb location to store data
Load package 1772474950.2909873 is LOADED and contains no failed jobs
```

## Questions

1. What is the start date and end date of the dataset?

```
import duckdb; 
con = duckdb.connect("/workspaces/data-engineering-zoomcamp-2026/taxi_pipeline.duckdb"); 
print(con.execute("SELECT MIN(trip_pickup_date_time) as start_date, MAX(trip_pickup_date_time) as end_date FROM nyc_taxi_data.taxi_data;").fetchall())
```
answer: 2009-06-01 to 2009-07-01

2. What proportion of trips are paid with credit card?
```
python3 -c 'import duckdb; con = duckdb.connect("/workspaces/data-engineering-zoomcamp-2026/taxi_pipeline.duckdb"); print(con.execute("SELECT payment_type, COUNT(*) FROM nyc_taxi_data.taxi_data GROUP BY payment_type;").fetchall())'

# Credit : 2 666 trips
# Cash : 7 332 trips (97 + 7 235)
# Other (No Charge, Dispute) : 2 trips
# Total : 10 000 trips
# 26,66 % (soit 2 666 / 10 000)
```
answer: 26.66%

3. What is the total amount of money generated in tips?
```
python3 -c 'import duckdb; con = duckdb.connect("/workspaces/data-engineering-zoomcamp-2026/taxi_pipeline.duckdb"); print(con.execute("SELECT SUM(tip_amt) FROM nyc_taxi_data.taxi_data;").fetchall())'
```
answer: $6,063.41