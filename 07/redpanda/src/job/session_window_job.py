from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_source(t_env):
    table_name = "events"
    t_env.execute_sql(f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            lpep_pickup_datetime BIGINT,
            event_timestamp AS TO_TIMESTAMP_LTZ(lpep_pickup_datetime, 3),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        );
    """)
    return table_name


def create_sink(t_env):
    table_name = "green_trips_session_windowed"
    t_env.execute_sql(f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            PULocationID INT,
            num_trips BIGINT,
            PRIMARY KEY (window_start, window_end, PULocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres'
        );
    """)
    return table_name


def run_session_job():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    t_env.get_config().set("execution.checkpointing.tolerable-failed-checkpoints", "10")
    
    source_table = create_source(t_env)
    aggregated_table = create_sink(t_env)

    t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT 
            window_start, 
            window_end, 
            PULocationID, 
            COUNT(*) as num_trips
        FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES)
        )
        GROUP BY window_start, window_end, PULocationID
    """).wait()


if __name__ == "__main__":
    run_session_job()
