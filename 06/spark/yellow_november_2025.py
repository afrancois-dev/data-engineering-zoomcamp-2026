import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read.parquet('yellow_tripdata_2025-11.parquet')

df.repartition(4).write.parquet('yellow_2025_11_repartitioned', mode='overwrite')

from pyspark.sql import functions as F

# Filter for trips starting on the 15th of November
trips_15th = df.filter(F.to_date(df.tpep_pickup_datetime) == '2025-11-15')
print(f"Number of trips on November 15th: {trips_15th.count()}")
