from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("StockPriceStreamer") \
    .getOrCreate()

# Define expected JSON schema
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType()) \
    .add("timestamp", LongType())

# Read stream from the socket (host = 'producer', port = 9999)
raw_df = spark.readStream \
    .format("socket") \
    .option("host", "producer") \
    .option("port", 9998) \
    .load()

# Parse the JSON text into structured columns
parsed_df = raw_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Write the stream to Parquet format
query = parsed_df.writeStream \
    .format("parquet") \
    .option("path", "/app/shared_volume/parquet_output") \
    .option("checkpointLocation", "/app/shared_volume/_checkpoint") \
    .outputMode("append") \
    .start()

# Keep the Spark job running
query.awaitTermination()
