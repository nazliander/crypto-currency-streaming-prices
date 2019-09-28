from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


class Source:
    def __init__(self):
        self.conf = SparkConf() \
            .setAppName("Crypto App") \
            .setMaster("spark://spark-master:7077")

        self.sc = SparkContext(conf=self.conf)

        self.spark = SparkSession.builder \
            .config(conf=self.conf) \
            .getOrCreate()

if __name__ == "__main__":
    s = Source()
    source = s.spark \
                .readStream \
                .format("kinesis") \
                .option("streamName", "crypto") \
                .option("endpointUrl", "localstack:4568") \
                .option("awsAccessKeyId", "kewl") \
                .option("awsSecretKey", "kewl") \
                .option("startingPosition", "LATEST") \
                .load()

    q = source \
            .writeStream \
            .queryName("dq") \
            .format("memory") \
            .start()

    raw = s.spark.sql("select * from dq")
    
    raw.show()

    raw.printSchema()

    q.awaitTermination()
