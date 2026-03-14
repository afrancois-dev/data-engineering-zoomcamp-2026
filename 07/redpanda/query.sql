CREATE TABLE processed_events (
    PULocationID INTEGER,
    DOLocationID INTEGER,
    trip_distance DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    passenger_count INTEGER,
    total_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP
);

select count(1) from processed_events;