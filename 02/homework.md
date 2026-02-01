# kestra

NB: I used backfill functionality to get data for both dataset from 2021-01 to 2021-07

1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?
```
- Kestra UI -> Triggers -> backfill from 2020-12-01 00:00:00 to 2020-12-02 00:00:00 in order to get 2020-01
- Kestra UI -> Execution (pipeline corresponding to 2021-12) -> Outputs -> extract tasks -> outputFiles -> yellow_tripdata_2020_12.csv -> 128.3MiB on the UI 
```
answer: 128.3MiB

2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
```
- Kestra UI -> Execution (pipeline corresponding to 2020-04) -> extract task -> outputFiles -> click on Debug Expression button -> 
{
  "green_tripdata_2020-04.csv": "kestra:///zoomcamp/05-postgres-taxi-scheduled/executions/22y71Ya1xzWhKlYpVw0a1j/tasks/extract/knP3ACuJGYMgmtiBcMqL7/6jMXP1UiFm5s0MQAGAZ0Gd-green_tripdata_2020-04.csv"
}
```
answer: green_tripdata_2020-04.csv


3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
Question to myself: how many rows in the database or in the file ? 

First of all, as usual : 
- Kestra UI -> Triggers -> backfill from 2020-01-01 00:00:00 to 2020-12-02 00:00:00 for both taxi (i.e yellow and green)

On pgadmin : 
```
SELECT count(*) 
FROM yellow_tripdata
WHERE filename ILIKE 'yellow_tripdata_2020-%.csv';
-- 24648499

```
answer: 24,648,499

4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

On pgadmin : 
```
SELECT count(*) 
FROM green_tripdata
WHERE filename ILIKE 'green_tripdata_2020-%.csv';
-- 1734051
```
answer: 1734051

5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

On Kestra UI -> Execution -> Metrics -> 

```
yellow_copy_in_to_staging_table rows 1,925,152
```

NB: Not the best solution. On my mind, the best way is to check directly in the file as some rows might not be extracted.

answer: 1,925,152

6. How would you configure the timezone to New York in a Schedule trigger?
- I checked the doc below
  - https://kestra.io/docs/workflow-components/triggers/schedule-trigger

answer: Add a timezone property set to America/New_York in the Schedule trigger configuration