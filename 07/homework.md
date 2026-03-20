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
- 1. re-create topic : 
```bash
docker exec -it redpanda-redpanda-1 rpk topic delete green-trips && docker exec -it redpanda-redpanda-1 rpk topic create green-trips
```

- 2. create table green_trips_session_windowed
```sql
CREATE TABLE IF NOT EXISTS green_trips_session_windowed (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, window_end, PULocationID)
);
```

- 3. run producer (through the producer.ipynb notebook)

- 4. flink job execution 
```bash
docker exec -it redpanda-jobmanager-1 flink run -py /opt/src/job/session_window_job.py
```

- 5. run pgsql query
```sql
-- uvx pgcli -h localhost -p 5432 -U postgres -d postgres
postgres@localhost:postgres> SELECT num_trips, window_start, window_end 
 FROM green_trips_session_windowed 
 ORDER BY num_trips DESC LIMIT 5;
+-----------+---------------------+---------------------+
| num_trips | window_start        | window_end          |
|-----------+---------------------+---------------------|
| 122       | 2025-10-01 06:51:02 | 2025-10-01 09:42:55 |
| 54        | 2025-10-24 10:11:50 | 2025-10-24 13:03:46 |
| 47        | 2025-10-19 17:00:30 | 2025-10-19 18:17:02 |
| 38        | 2025-10-07 17:22:13 | 2025-10-07 19:03:39 |
| 36        | 2025-10-29 10:21:44 | 2025-10-29 12:15:29 |
+-----------+---------------------+---------------------+
```
answer: 

6. Tumbling window - largest tip
- 1. re-create topic : 
```bash
docker exec -it redpanda-redpanda-1 rpk topic delete green-trips && docker exec -it redpanda-redpanda-1 rpk topic create green-trips
```

- 2. create table green_trips_tumble_windowed_1h
```sql
CREATE TABLE green_trips_tumble_windowed_1h (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    total_tips DOUBLE PRECISION,
    PRIMARY KEY (window_start)
);
```

- 3. run producer (through the producer.ipynb notebook)

- 4. flink job execution 
```bash
docker exec -it redpanda-jobmanager-1 flink run -py /opt/src/job/tumbling_window_1h_job.py
```

- 5. run pgsql query
```sql
postgres@localhost:postgres> SELECT 
     window_start, 
     total_tips 
 FROM 
     green_trips_tumble_windowed_1h 
 ORDER BY 
     total_tips DESC 
 LIMIT 5;
+---------------------+--------------------+
| window_start        | total_tips         |
|---------------------+--------------------|
| 2025-10-16 18:00:00 | 510.8599999999999  |
| 2025-10-30 16:00:00 | 507.1              |
| 2025-10-09 18:00:00 | 472.01000000000016 |
| 2025-10-10 17:00:00 | 470.0800000000002  |
| 2025-10-16 17:00:00 | 445.01000000000005 |
+---------------------+--------------------+
```
answer: 2025-10-16 18:00:00