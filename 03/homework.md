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
```
SELECT count(*) FROM endless-office-485017-f8.dwh_taxi.external_yellow_tripdata;
-- 20332093
```
answer: 20,332,093

2. Data read estimation
```
-- scanning 0 Mo
SELECT count(distinct(PULocationID)) FROM endless-office-485017-f8.dwh_taxi.external_yellow_tripdata;

-- scanning 155.12 Mo
SELECT count(distinct(PULocationID)) FROM endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned;
```
answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

3. Understanding columnar storage
```
-- 155,12 Mo scanned
SELECT PULocationID FROM endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned;

-- 310,24 Mo scanned
SELECT PULocationID, DOLocationID FROM endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned;
```
answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

4. Counting zero fare trips
```
SELECT count(*) FROM endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned
where fare_amount = 0;
```
answer: 8,333

5. Partitioning and clustering
- Always filtering by a timestamp -> partitioning is the most effective way to reduce amound of data scanned
- We need to "order the results" by VendorID -> clustering is the ideal choice. Clustering sort the data within each partition based on the specified column.
```
-- creating optimized table
CREATE OR REPLACE TABLE `endless-office-485017-f8.dwh_taxi.yellow_tripdata_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned`;
```
answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

6. Partition benefits

```
-- Scanning 310,24 Mo
select distinct(VendorID) from  `endless-office-485017-f8.dwh_taxi.yellow_tripdata_non_partitioned` 
where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15'

-- Scanning 26,84 Mo
select distinct(VendorID) from  `endless-office-485017-f8.dwh_taxi.yellow_tripdata_optimized` 
where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15'
```
answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

7. External table storage
cf. create statement in the beforehand section
answer: GCP Bucket

8. Clustering best practices
Clustering should be used when : 
- the table is large (e.g > 1Go)
- query filtering or aggregation is highely used for specific columns
Otherwise, the result can actually hinder performance or provide no benefit at all

answer: False

9. Understanding table scans
```
-- scanning 0 bytes
select count(*) from  `endless-office-485017-f8.dwh_taxi.yellow_tripdata_optimized` 
```
No execution is required because the number of row is already contained in the metadata table.