

from pyspark.sql.functions import (from_json, col)

from spark_base import Source
from schema.crypto_models import crypto_model_schema


def connect_to_kafka_stream(topic_name, spark_session):
    return (spark_session
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "http://kafka:29092")
            .option("subscribe", topic_name)
            .load())


def get_crypto_values_query(dataframe):
    return (df.selectExpr("CAST(value AS STRING) AS json")
              .select(
                  from_json(col("json"), crypto_model_schema).alias("data"))
              .select("data.*"))


if __name__ == "__main__":

    s = Source()
    s.sc.setLogLevel("INFO")
    df = connect_to_kafka_stream(topic_name="crypto", spark_session=s.spark)
    crypto_values = get_crypto_values_query(df)
    query = crypto_values \
        .writeStream \
        .option("truncate", "false") \
        .outputMode("append") \
        .format("console") \
        .start()
    query.awaitTermination()
