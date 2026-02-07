# dwh

## beforehand
- on the GCP UI (GCS) : 
  - create bucket
    - gs://dwh-yellowtrip-data
- on Codespace
  - gcloud auth application-default login
- use the load_yellow_taxi_data.py
  - local auth based on my personal service account
  - changed bucket name
  - `uv run load_yellow_taxi_data.py`

on Bigquery
- create bigquery dataset
  - 
- load data using external table, here it means bigquery will get data from gcs
  - pattern : gs://dwh-yellowtrip-data/yellow_tripdata_2024-*.parquet
```
CREATE OR REPLACE EXTERNAL TABLE `endless-office-485017-f8.dwh_taxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dwh-yellowtrip-data/yellow_tripdata_2024-*.parquet']
);
```
- create a regular table from external table : 
```
CREATE OR REPLACE TABLE endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned AS
SELECT * FROM endless-office-485017-f8.dwh_taxi.external_yellow_tripdata;
```
1. Counting records

