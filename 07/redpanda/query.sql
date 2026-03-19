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

-- question 4
CREATE TABLE IF NOT EXISTS green_trips_tumble_windowed (
    window_start TIMESTAMP(3), 
    PULocationID INT, 
    num_trips BIGINT, 
    PRIMARY KEY (window_start, PULocationID)
);

-- question 5
CREATE TABLE IF NOT EXISTS green_trips_session_windowed (
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, window_end, PULocationID)
);