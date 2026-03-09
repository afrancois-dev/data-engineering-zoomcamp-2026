# Spark

## Beforehand (set-up)
- Install java and pyspark
- run pyspark test : `uv run python test_spark.py`


## Questions

1. Install Spark and PySpark 

```
@afrancois-dev ➜ /workspaces/data-engineering-zoomcamp-2026/06/spark (main) $ uv run test_spark.py 
WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
26/03/09 16:36:20 WARN Utils: Your hostname, codespaces-32dc43, resolves to a loopback address: 127.0.0.1; using 10.0.3.15 instead (on interface eth0)
26/03/09 16:36:20 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/03/09 16:36:21 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark version: 4.1.1
+---+
| id|
+---+
|  0|
|  1|
|  2|
|  3|
|  4|
|  5|
|  6|
|  7|
|  8|
|  9|
+---+
```
answer: Spark version: 4.1.1

2. Yellow November 2025

```
@afrancois-dev ➜ .../data-engineering-zoomcamp-2026/06/spark/yellow_2025_11_repartitioned (main) $ ls -lah
total 99M
drwxr-xr-x+ 2 codespace codespace 4.0K Mar  9 16:34 .
drwxrwxrwx+ 4 codespace codespace 4.0K Mar  9 16:34 ..
-rw-r--r--  1 codespace codespace    8 Mar  9 16:34 ._SUCCESS.crc
-rw-r--r--  1 codespace codespace 196K Mar  9 16:34 .part-00000-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet.crc
-rw-r--r--  1 codespace codespace 196K Mar  9 16:34 .part-00001-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet.crc
-rw-r--r--  1 codespace codespace 196K Mar  9 16:34 .part-00002-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet.crc
-rw-r--r--  1 codespace codespace 196K Mar  9 16:34 .part-00003-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet.crc
-rw-r--r--  1 codespace codespace    0 Mar  9 16:34 _SUCCESS
-rw-r--r--  1 codespace codespace  25M Mar  9 16:34 part-00000-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet
-rw-r--r--  1 codespace codespace  25M Mar  9 16:34 part-00001-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet
-rw-r--r--  1 codespace codespace  25M Mar  9 16:34 part-00002-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet
-rw-r--r--  1 codespace codespace  25M Mar  9 16:34 part-00003-c510cb3f-05e5-4f29-a471-389ac0e845d2-c000.snappy.parquet
```

