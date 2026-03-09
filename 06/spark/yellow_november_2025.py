import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read.parquet('yellow_tripdata_2025-11.parquet')

df.repartition(4).write.parquet('yellow_2025_11_repartitioned', mode='overwrite')



# Question 2. Filter for trips starting on the 15th of November
trips_15th = df.filter(F.to_date(df.tpep_pickup_datetime) == '2025-11-15')
print(f"Number of trips on November 15th: {trips_15th.count()}")

# Question 3. Longest trip in hours
df_duration = df.withColumn('duration_hours', 
    (F.unix_timestamp('tpep_dropoff_datetime') - F.unix_timestamp('tpep_pickup_datetime')) / 3600
)
max_duration = df_duration.select(F.max('duration_hours')).collect()[0][0]
print(f"Longest trip duration in hours: {max_duration}")

# Question 4. Least frequent pickup location Zone
df_zones = spark.read.csv('taxi_zone_lookup.csv', header=True, inferSchema=True)

df.createOrReplaceTempView('yellow_tripdata')
df_zones.createOrReplaceTempView('zones')

least_frequent_pickup = spark.sql("""
    SELECT
        z.Zone,
        count(1) AS count
    FROM
        yellow_tripdata t
    JOIN
        zones z ON t.PULocationID = z.LocationID
    GROUP BY
        z.Zone
    ORDER BY
        count ASC
    LIMIT 10
""")

least_frequent_pickup.show()
