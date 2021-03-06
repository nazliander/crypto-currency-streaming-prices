from pyspark.sql.functions import (
    from_json, col, window, avg, desc, max, min)

from spark_base import Source
from schema.crypto_models import crypto_model_schema


def connect_to_kafka_stream(topic_name, spark_session):
    return (spark_session
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "http://kafka:29092")
            .option("subscribe", topic_name)
            .load())


def calculate_simple_moving_average(dataframe):
    w = window(
        timeColumn="date_time",
        windowDuration="60 seconds",
        slideDuration="20 seconds")
    # Milliseconds to UTC
    return (df
            .selectExpr("CAST(value AS STRING) AS json")
            .select(
                from_json(col("json"), crypto_model_schema).alias("data"))
            .select(
                "data.*",
                (col("data.timestamp_logger")/1000).cast(
                    "timestamp").alias("date_time"))
            .withWatermark("date_time", "20 seconds")
            .groupBy(col("nameCoin"), w)
            .agg(avg("price"))
            .select(
                "nameCoin",
                "window",
                col("avg(price)").alias("simple_moving_average_price"))
            )


if __name__ == "__main__":
    s = Source()
    s.sc.setLogLevel("ERROR")
    df = connect_to_kafka_stream(
        topic_name="crypto_raw", spark_session=s.spark)
    crypto_values = calculate_simple_moving_average(df)

    query = (crypto_values
             .writeStream
             .option("truncate", "false")
             .outputMode("append")
             .format("console")
             .start()
             )
    query.awaitTermination()
