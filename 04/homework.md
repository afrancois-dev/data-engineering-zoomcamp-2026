# dbt 

## Beforehand
Data loaded based on cloud setup guide
```
-- Creating external table referring to gcs path for yellow / green
CREATE OR REPLACE EXTERNAL TABLE `endless-office-485017-f8.dwh_taxi.external_yellow_tripdata_2019_2020`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dwh-trip-data/yellow_tripdata_2019-*.csv.gz', 'gs://dwh-trip-data/yellow_tripdata_2020-*.csv.gz']
);
-- regular table
CREATE OR REPLACE TABLE `endless-office-485017-f8.dwh_taxi.yellow_tripdata` AS
SELECT * FROM `endless-office-485017-f8.dwh_taxi.yellow_tripdata_2019_2020`

CREATE OR REPLACE EXTERNAL TABLE `endless-office-485017-f8.dwh_taxi.external_green_tripdata_2019_2020`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dwh-trip-data/green_tripdata_2019-*.csv.gz', 'gs://dwh-trip-data/green_tripdata_2020-*.csv.gz']
);
-- regular table
CREATE OR REPLACE TABLE `endless-office-485017-f8.dwh_taxi.green_tripdata_2019_2020` AS
SELECT * FROM `endless-office-485017-f8.dwh_taxi.green_tripdata`
```

NB: I had to rename every ny_taxi occurences for the bigquery dataset within the dbt files.

## Questions
1. dbt Lineage and Execution

```
19:36:57
1 of 1 START sql view model dbt_prod.int_trips_unioned ......................... [RUN]
19:36:58
1 of 1 OK created sql view model dbt_prod.int_trips_unioned .................... [CREATE VIEW (0 processed) in 1.07s]
```
answer: int_trips_unioned only

2. dbt Tests

```
-- removed 5 on the list
dbt run --select fct_trips
dbt test --select fct_trips

-- dbt fails
19:59:27
1 of 10 START test accepted_values_fct_trips_payment_type__False__1__2__3__4 ... [RUN]
19:59:29
1 of 10 FAIL 1 accepted_values_fct_trips_payment_type__False__1__2__3__4 ....... [FAIL 1 in 1.73s]
19:59:31
Failure in test accepted_values_fct_trips_payment_type__False__1__2__3__4 (models/marts/schema.yml)
19:59:31
  Got 1 result, configured to fail if != 0
19:59:31
  compiled code at target/compiled/taxi_rides_ny/models/marts/schema.yml/accepted_values_fct_trips_payment_type__False__1__2__3__4.sql
```
answer: dbt will fail the test, returning a non-zero exit code

3. Counting Records in fct_monthly_zone_revenue
```
-- once dbt run
SELECT count(*) FROM `endless-office-485017-f8.dbt_prod.fct_monthly_zone_revenue`
-- 12184 rows
```
anwer: 12184

4. Best Performing Zone for Green Taxis (2020)
```
SELECT pickup_zone, max(revenue_monthly_total_amount) FROM `endless-office-485017-f8.dbt_prod.fct_monthly_zone_revenue`
where service_type = 'Green' and revenue_month >= '2020-01-01' and revenue_month < '2021-01-01'
group by pickup_zone
order by 2 desc
limit 1
-- Line	pickup_zone	f0_
-- 1	East Harlem North	434613.66	
```
answer: East Harlem North


5. Green Taxi Trip Counts (October 2019)
```
SELECT sum(total_monthly_trips) FROM `endless-office-485017-f8.dbt_prod.fct_monthly_zone_revenue`
where service_type = 'Green' and revenue_month >= '2019-10-01' and revenue_month < '2019-11-01'
-- 384624
```
answer: 384,624

6. Build a Staging Model for FHV Data
```
-- 1. run python script load_green_yellow_fhv_taxi_data.py
-- 2. Creating external table referring to gcs path for yellow / green
CREATE OR REPLACE EXTERNAL TABLE `endless-office-485017-f8.dwh_taxi.external_fhv_2019`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dwh-trip-data/fhv_tripdata_2019-*.csv.gz']
);
-- 3. regular table
CREATE OR REPLACE TABLE `endless-office-485017-f8.dwh_taxi.fhv_tripdata` AS
SELECT * FROM `endless-office-485017-f8.dwh_taxi.external_fhv_2019`

-- 4. staging/sources.yml
      - name: fhv_tripdata
        description: fhv taxi trip records
        columns:
          - name: dispatching_base_num
          - name: pickup_datetime
          - name: dropoff_datetime
          - name: pulocationid
          - name: dolocationid
          - name: sr_flag
          - name: affiliated_base_number

-- 5. staging/stg_fhv_tripdata.sql

with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers
        cast(dispatching_base_num as string) as dispatching_base_num,
        cast(affiliated_base_number as string) as affiliated_base_number,

        -- timestamps
        cast(pickup_datetime as timestamp) as pickup_datetime,  -- lpep = Licensed Passenger Enhancement Program (green taxis)
        cast(dropoff_datetime as timestamp) as dropoff_datetime,

        -- trip info
        cast(dolocationid as integer) as dropoff_location_id,
        cast(sr_flag as string) as sr_flag
        cast(pulocationid as integer) as pickup_location_id,

        -- payment info
    from source
    -- Filter out records with null dispatching_base_num (data quality requirement)
    where dispatching_base_num is not null
)

select * from renamed

-- Sample records for dev environment using deterministic date filter
{% if target.name == 'dev' %}
where pickup_datetime >= '2019-01-01' and pickup_datetime < '2019-02-01'
{% endif %}

6. exec. run command within dbt
dbt run --select stg_fhv_tripdata
20:53:11
1 of 1 START sql view model dbt_prod.stg_fhv_tripdata .......................... [RUN]
20:53:12
1 of 1 OK created sql view model dbt_prod.stg_fhv_tripdata ..................... [CREATE VIEW (0 processed) in 0.98s]

7. exec. query on bigquery
SELECT count(*) FROM `endless-office-485017-f8.dbt_prod.stg_fhv_tripdata` LIMIT 1000
-- 43244693
```
answer: 43,244,693
