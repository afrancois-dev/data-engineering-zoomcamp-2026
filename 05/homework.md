# bruin

```
bruin validate ./pipeline/pipeline.yml
bruin run ./pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01
bruin run ./pipeline/pipeline.yml --full-refresh

```


1. Bruin Pipeline Structure
In a Bruin project, what are the required files/directories?
cf. https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-data-platforms/notes/06-core-02-pipelines.md
cf. https://github.com/bruin-data/bruin/tree/main/templates

answer:
.bruin.yml and pipeline/ with pipeline.yml and assets/

2. Materialization Strategies
You're building a pipeline that processes NYC taxi data organized by month based on pickup_datetime. Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

Same as the homework i.e time_interval -> time_interval strategy: deletes rows in the time window, then inserts the query result

answer:
time_interval - incremental based on a time column

3. Pipeline Variables
You have the following variable defined in pipeline.yml:
```
variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```
How do you override this when running the pipeline to only process yellow taxis?
cf. https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-data-platforms/notes/06-core-04-variables.md

```
@afrancois-dev ➜ .../data-engineering-zoomcamp-2026/05/bruin/my-pipeline (main) $ bruin run ./pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01 --var 'taxi_types=["yellow"]'
Analyzed the pipeline 'nyc_taxi' with 4 assets.

Pipeline: nyc_taxi (..)
  No issues found

✓ Successfully validated 4 assets across 1 pipeline, all good.

Interval: 2022-01-01T00:00:00Z - 2022-02-01T00:00:00Z

Starting the pipeline execution...
```


answer: `bruin run --var 'taxi_types=["yellow"]'`

4. Running with Dependencies
You've modified the ingestion/trips.py asset and want to run it plus all downstream assets. Which command should you use?


cf. https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-data-platforms/notes/06-core-05-commands.md

answer: `bruin run ingestion/trips.py --downstream`

5. Quality Checks
You want to ensure the pickup_datetime column in your trips table never has NULL values. Which quality check should you add to your asset definition?

Example:
```
columns:
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null
```

answer: `name: not_null`

6. Lineage and Dependencies
After building your pipeline, you want to visualize the dependency graph between assets. Which Bruin command should you use?
cf. https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-data-platforms/notes/06-core-05-commands.md
Example: `bruin lineage ./pipeline/pipeline.yml`

answer: `bruin lineage`

7. First-Time Run
You're running a Bruin pipeline for the first time on a new DuckDB database. What flag should you use to ensure tables are created from scratch?
cf. https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-data-platforms/notes/06-core-05-commands.md

answer: `--full-refresh`
