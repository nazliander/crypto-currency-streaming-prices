from pyspark.sql.types import (
    StructType, StringType, LongType)


crypto_model_schema = (StructType()
                       .add("nameCoin", StringType())
                       .add("symbolCoin", StringType())
                       .add("numberOfMarkets", LongType())
                       .add("volume", LongType())
                       .add("marketCap", LongType())
                       .add("totalSupply", LongType())
                       .add("price", StringType())
                       .add("timestamp_logger", LongType()))
