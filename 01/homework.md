
# Docker
## Question 1
```
docker run -it --entrypoint=bash python:3.13-slim
uv pip -V
```
answer : 25.3

## Question 2
```
docker-compose up
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --user=postgres \
    --password=postgres \
    --host=db \
    --port=5433 \
    --db=ny_taxi
```
answer: db=5432 (as pgadmin is inside docker-compose network, it should use the internal port)

## Question 3

```
select count(*) from green_trips
where lpep_pickup_datetime >= '2025-11-01' and lpep_pickup_datetime < '2025-12-01'
and trip_distance <= 1
```
answer: 8007

## Question 4

```
select lpep_pickup_datetime::date, max(trip_distance) as max_distance 
from green_trips
where trip_distance < 100
group by lpep_pickup_datetime::date
order by max_distance DESC
```
answer: 2025-11-14 (if we refer to the single longest individual trip)

## Question 5

```
SELECT
    count(*) as total_amount,
    zpu."Zone" AS "pickup_loc"
FROM
    green_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
where t.lpep_pickup_datetime::date = '2025-11-18'
group by pickup_loc
order by total_amount desc
limit 1
```
answer: East Harlem North

## Question 6
```
SELECT
    tip_amount,
    zdo."Zone" AS "dropoff_loc"
FROM
    green_trips t
INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
INNER JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
where t.lpep_pickup_datetime >= '2025-11-01' and t.lpep_pickup_datetime < '2025-12-01'
and zpu."Zone" = 'East Harlem North'
order by tip_amount desc
limit 1
```
answer: Yorkville West

# Terraform

## Question 7
```
terraform init, terraform apply -auto-approve, terraform destroy
```
