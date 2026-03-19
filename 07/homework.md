# Redpanda - Flink

## Beforehand
- set-up python (with uv)
 - `pip install uv`
 - `uv add kafka-python pandas pyarrow`
 - `uvx pgcli -h localhost -p 5432 -U postgres -d postgres`
- set-up docker
 - get the docker-compose.yml from github repo.
 - `docker compose up redpanda -d`
 - `docker compose logs redpanda -f`

- useful commands for redpanda
```
docker exec -it redpanda-redpanda-1 rpk topic delete rides && docker exec -it redpanda-redpanda-1 rpk topic create rides
```

We are going to 
    1. create a producer
    2. create a consumer

## Questions

1. Redpanda version
```
(redpanda) @afrancois-dev ➜ /workspaces/data-engineering-zoomcamp-2026/07/redpanda (main) $ docker exec -it redpanda-redpanda-1 rpk version
rpk version: v25.3.9
Git ref:     836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
Build date:  2026 Feb 26 07 48 21 Thu
OS/Arch:     linux/amd64
Go version:  go1.24.3

Redpanda Cluster
  node-1  v25.3.9 - 836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
```
answer: v25.3.9

2. Sending data to Redpanda

NB: lpep_pickup_datetime and lpep_dropofdatetime have been converted to int and then timestamp like the workshop

```
took 8.08 seconds
```


answer: 10 seconds (closest value from took 8.08 seconds)

3. Consumer - trip distance
- on pgcli
```
postgres@localhost:postgres> select count(*) from processed_events where trip_distance > 5;
+-------+
| count |
|-------|
| 8506  |
+-------+
SELECT 1
Time: 0.004s
```

answer: 8506

4. Tumbling window - pickup location
- 1. re-create topic : 
```
docker exec -it redpanda-redpanda-1 rpk topic delete green-trips && docker exec -it redpanda-redpanda-1 rpk topic create green-trips
# (Optional) truncate the table on pgsql if several runs
# TRUNCATE TABLE green_trips_tumble_windowed;


```

- 2. create table green_trips_tumble_windowed
```
CREATE TABLE IF NOT EXISTS green_trips_tumble_windowed (
    window_start TIMESTAMP(3), 
    PULocationID INT, 
    num_trips BIGINT, 
    PRIMARY KEY (window_start, PULocationID)
);
```

- 3. Run producer (trough the producer.ipynb notebook)
- 4. flink job execution 
```
docker exec -it redpanda-jobmanager-1 flink run -py /opt/src/job/tumbling_window_job.py
```
- 5. run pgsql query
```
# uvx pgcli -h localhost -p 5432 -U postgres -d postgres
postgres@localhost:postgres> SELECT PULocationID, num_trips
 FROM green_trips_tumble_windowed
 ORDER BY num_trips DESC
 LIMIT 3;
+--------------+-----------+
| pulocationid | num_trips |
|--------------+-----------|
| 74           | 15        |
| 74           | 14        |
| 74           | 13        |
+--------------+-----------+
```
answer: 74

5. Session window - longest streak

- 2. Create table

```
CREATE TABLE IF NOT EXISTS green_trips_session_windowed (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, window_end, PULocationID)
);
```
- Run job
```
docker exec -it redpanda-jobmanager-1 flink run -py /opt/src/job/session_window_job.py
```

- execute query
```
postgres@localhost:postgres> SELECT PULocationID, num_trips, (window_end - window_start) as session_du
 ration
 FROM green_trips_session_windowed
 ORDER BY num_trips DESC
 LIMIT 5;
+--------------+-----------+------------------+
| pulocationid | num_trips | session_duration |
|--------------+-----------+------------------|
| 74           | 734       | 13:10:20         |
| 74           | 422       | 17:31:46         |
| 74           | 416       | 17:15:16         |
| 74           | 411       | 14:37:29         |
| 74           | 407       | 14:46:44         |
+--------------+-----------+------------------+
SELECT 5
Time: 0.020s
```

answer: