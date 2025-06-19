from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

spark = SparkSession.builder.appName("StockFileStreamer").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType()) \
    .add("timestamp", LongType())

print("[spark] ✅ Starting file stream...")
df = spark.readStream \
    .schema(schema) \
    .json("/app/shared_volume/stream_data")

df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/app/shared_volume/checkpoints") \
    .option("path", "/app/shared_volume/parquet_output") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
